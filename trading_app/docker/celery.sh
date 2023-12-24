#!/bin/bash

cd src


if [[ "$1" == "celery" ]]; then
  echo "[+] Starting Celery Worker..."
  celery --app=tasks.tasks:celery worker -l INFO
elif [[ "$1" == "flower" ]]; then
  echo "[+] Starting Flower..."
  celery --app=tasks.tasks:celery flower
  fi

    