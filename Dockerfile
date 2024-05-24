FROM python:3.12

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

COPY ./system_cars .

RUN mkdir -p applications/static/reports

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]