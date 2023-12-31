FROM python:3.10-slim

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt

COPY . /app

ENV PORT 8501

CMD ["streamlit", "run", "app.py"]