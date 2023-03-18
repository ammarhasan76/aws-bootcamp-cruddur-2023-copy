FROM python:3.10-slim-buster

# Inside Container
WORKDIR /backend-flask

# Local host filesystem that has repo -> Container filesystem
COPY requirements.txt requirements.txt

# Inside Container
# Install the Python Libraries used for the app
RUN pip3 install -r requirements.txt

# Cope everything from current local directory -> Container filesystem
COPY . .

# Environment Variable inside Container
ENV FLASK_ENV=development

# Expost port in the container
EXPOSE ${PORT}

# Command executed in container (run flask process)
# python3 -m flask run --host=0.0.0.0 --port=4567
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]