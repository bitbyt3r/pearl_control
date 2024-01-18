# pull official base image
FROM python

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip poetry
COPY . /app/
RUN poetry install

CMD ["poetry", "run", "pearl_control", "--url", "http://${IP}", "--username", "${USERNAME}", "--password", "${PASSWORD}", "--name", "${NAME}"]
