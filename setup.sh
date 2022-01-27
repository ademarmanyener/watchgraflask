#!/bin/sh

PWD=`pwd`
VIRTENV_FOLDER=virtualenv/
REQS_TXT=requirements.txt

print_title () {
  clear
  echo "[WatchGraf - watchgraflask setup script]"
  echo "========================================"
}

check_virtenv () {
  if [ ! -d $VIRTENV_FOLDER ]
  then
    python3 -m virtualenv virtualenv
    return_check_virtenv=0
  else
    echo "\n$VIRTENV_FOLDER exists.\n"
    return_check_virtenv=1
    :
  fi
}

install_reqs () {
  if [ $return_check_virtenv -eq 1 ]
  then
    cat $REQS_TXT
    read -p "You want to download the packages above? [y/N]: " getread
    if [ $getread ]
    then
      if [ $getread = "y" ] || [ $getread = "Y" ]
      then
        python3 -m pip install $(cat $REQS_TXT)
      else
        echo "\nCancelled."
        exit
      fi
    else
      echo "\nCancelled."
      exit
    fi
  else
    :
  fi
}

create_db () {
  if [ ! -d db/ ]
  then
    mkdir -p db/
  fi
  python3 -c "from includes import *;db.create_all();"
}

print_title
check_virtenv
install_reqs
create_db
