FROM python:3.10-slim

RUN pip install virtualenv
ENV VIRTUAL_ENV=/venv
RUN virtualenv venv -p python3
ENV PATH="VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
ADD . /app

# Install dependencies
RUN pip install -r requirements.txt

# copying all files over
COPY . /app

# Expose port 
ENV PORT 8501

# cmd to launch app when container is run
CMD ["streamlit", "run", "app.py"]