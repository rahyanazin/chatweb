FROM python:3.9-slim

WORKDIR /code

COPY ./app /code

RUN pip install streamlit requests

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py"]