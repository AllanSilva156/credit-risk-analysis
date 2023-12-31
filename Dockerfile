FROM python:3.10-slim

RUN git clone https://github.com/streamlit/streamlit-example.git .

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]