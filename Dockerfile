FROM python:3.10-slim

COPY ./requirements.txt /usr/requirements.txt

WORKDIR /usr

RUN pip install -r requirements.txt

COPY ./app /usr/app
COPY ./pipelines /usr/pipelines

ENV PORT 8501

ENTRYPOINT ["python3"]

CMD ["streamlit", "run", "app/app.py"]
