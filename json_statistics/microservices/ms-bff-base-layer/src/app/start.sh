#! /bin/sh
gunicorn app:app --bind :5000 --log-level=$LOG_LEVEL --timeout $TIMEOUT --reload 

