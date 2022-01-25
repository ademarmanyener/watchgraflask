#!/bin/sh

export FLASK_APP=run_app.py

if [ $1 ];
then
  if [ $1 = "--debug" ];
  then
    export FLASK_DEBUG=True
  fi
else
  export FLASK_DEBUG=False
fi

flask run
