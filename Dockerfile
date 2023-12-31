FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/streamlit/streamlit-example.git

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app/app.py"]