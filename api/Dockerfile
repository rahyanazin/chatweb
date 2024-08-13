FROM python:3.9-slim

WORKDIR /code

COPY . /code

# RUN pip install fastapi uvicorn

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]