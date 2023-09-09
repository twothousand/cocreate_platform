FROM python:3.9.17
LABEL authors="puppet"

ENTRYPOINT ["top", "-b"]