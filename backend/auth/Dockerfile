FROM python:3.9

WORKDIR /app

EXPOSE 5000

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

COPY . ./

CMD ["python", "models.py", "app.py"]