########################
###    zsh config    ###

### default zsh config
. "$HOME/.local/bin/env"

### enable `#` as comments - https://stackoverflow.com/a/11873793/8213085
setopt interactivecomments


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

### disable pip update warning
PIP_DISABLE_PIP_VERSION_CHECK=1

### change text editor  (default is Vim)
EDITOR=nano
VISUAL=$EDITOR

### direnv setup for zsh
eval "$(direnv hook zsh)"

### load .env file at dir  (use direnv instead)
#if source $PWD/.env &> /dev/null; then
#  echo -e "\033[1;32mSuccessfully loaded .env file at $PWD\033[0m"
#fi

### set custom aliases
get-no() {
  echo "\033[0;34m$(curl https://naas.isalman.dev/no --silent | jq --raw-output '.reason')\033[0m"
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

### flag "incorrect" git remotes  (I only want SSH remotes formatted in a specific way)
flag-git-remote() {
  PATTERN_HTTP='^https:\/\/github\.com\/([0-9A-Za-z_-]+)\/([0-9A-Za-z_-]+)(\.git)?$'
  PATTERN_SSH='^git@github.com:\/?([0-9A-Za-z_-]+)\/([0-9A-Za-z_-]+)(.git)?$'
  REPLACE='git@github.com:\1\/\2'
  REMOTE_NAME='origin'
  CURRENT_URL=$(git remote get-url $REMOTE_NAME 2>/dev/null)
  NORMALISED_URL=$(git remote get-url $REMOTE_NAME | sed -E "s/$PATTERN_HTTP/$REPLACE/" | sed -E "s/$PATTERN_SSH/$REPLACE/")

  if [[ $CURRENT_URL != $NORMALISED_URL ]]; then
    echo "\033[1;31mincorrect remote detected:\033[0m $CURRENT_URL"
    echo "\033[1;31mrun the following to fix it:\033[0m git remote set-url $REMOTE_NAME $NORMALISED_URL"
  fi
}
flag-git-remote


############################
###    CLI completion    ###

### dbt completion  (https://github.com/dbt-labs/dbt-completion.bash#installation-bash-script-on-zsh)

if ! [[ -f ~/.dbt-completion.bash ]]; then
  curl https://raw.githubusercontent.com/dbt-labs/dbt-completion.bash/master/dbt-completion.bash > ~/.dbt-completion.bash
fi
autoload -U +X compinit && compinit
autoload -U +X bashcompinit && bashcompinit
source ~/.dbt-completion.bash
