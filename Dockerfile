FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

COPY app.py /app/app.py

COPY /pipelines /app/pipelines

COPY /img /app/img

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]