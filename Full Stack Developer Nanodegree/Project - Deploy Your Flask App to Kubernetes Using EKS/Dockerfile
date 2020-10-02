# source image
FROM python:stretch

# copy files to image
COPY . /app

# set work directory
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install flask
RUN pip install -r requirements.txt

EXPOSE 8080

# excecute command
ENTRYPOINT ["gunicorn", "-b", ":8080", "main:APP"]