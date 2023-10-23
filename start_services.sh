#!/bin/bash

start_celery() {
    celery -A Pecunya.Home worker --loglevel=debug &
    sleep 10
    celery -A Home call CeleryTasks.tasks.listen_to_blockchain_task &
}

start_django() {
    daphne Home.asgi:application -b 0.0.0.0 -p 8000
}

start_celery
start_django
