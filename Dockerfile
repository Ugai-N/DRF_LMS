FROM python:3
WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
#CMD ["python", "manage.py", "runserver"] - это выполняется уже в докер-компоуз