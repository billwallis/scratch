########################
###    zsh config    ###

### default zsh config
. "$HOME/.local/bin/env"

### enable plugins
# plugins=(
# 	git
# 	docker
# 	zsh-autosuggestions
# 	zsh-syntax-highlighting
# 	zsh-history-substring-search
# 	last-working-dir
# 	z
# 	aws
# 	minikube
# 	terraform
# )


##############################
###    Custom shadizzle    ###

### change text editor  (default is Vim)
EDITOR=nano
VISUAL=$EDITOR

### direnv setup for zsh
eval "$(direnv hook zsh)"

### load .env file at dir  (use direnv instead)
#if source $PWD/.env &> /dev/null; then
#    echo -e "\033[1;32mSuccessfully loaded .env file at $PWD\033[0m"
#fi

### set custom aliases
get-no() {
    echo "\033[0;34m$(curl https://naas.isalman.dev/no --silent | jq .reason)\033[0m"
}

### change terminal prompt  (https://stackoverflow.com/q/67587439/8213085)
precmd() {
  if [[ -n "$VIRTUAL_ENV" ]];
    then venv=" ($(basename $VIRTUAL_ENV))"
    else venv=""
  fi
  git check-ignore -q . 2>/dev/null; if [ "$?" -ne "1" ];
    then branch=""
    else branch=" $(git branch --show-current)"
  fi
  PROMPT="%{%F{blue}%}%n%{%f%} @ %{%F{yellow}%}%2~%{%f%}%F{green}$branch%{%f%}%{%F{#808080}$venv%f%}"$'\n'"%# "
}

### flag HTTPS git remotes
flag-http-git-remote() {
  remote=$(git remote get-url origin 2>/dev/null)
  if [[ -n $remote ]];
    then if [[ $remote == http* ]];
      then echo "\033[1;31mhttp remote detected: $remote\033[0m"
    fi
  fi
}
flag-http-git-remote


############################
###    CLI completion    ###

### dbt completion  (https://github.com/dbt-labs/dbt-completion.bash#installation-bash-script-on-zsh)

if ! [[ -f ~/.dbt-completion.bash ]]; then
  curl https://raw.githubusercontent.com/dbt-labs/dbt-completion.bash/master/dbt-completion.bash > ~/.dbt-completion.bash
fi
autoload -U +X compinit && compinit
autoload -U +X bashcompinit && bashcompinit
source ~/.dbt-completion.bash
