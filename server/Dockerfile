#ADD BASE IMAGE
FROM python:3.8.2

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y netcat

ENV APP=/app

#CHANGE WORKDIR
WORKDIR $APP

#INSTALL REQUIREMENTS AND UPGRADE PIP
COPY requirements.txt $APP
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#COPY THE REST OF THE FILES
COPY . $APP

#EXPOSE ON PORT 8000
EXPOSE 8000

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]