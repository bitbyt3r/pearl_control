# pull official base image
FROM python

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY . /app/
RUN pip install .

CMD ["python", "-m", "pearl_control", "--url", "http://${IP}", "--username", "${USERNAME}", "--password", "${PASSWORD}", "--name", "${NAME}"]
