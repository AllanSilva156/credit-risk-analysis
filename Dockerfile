FROM python:3.10-slim

WORKDIR /app

# Copiar todos os arquivos para /app
COPY . .

# Instalar dependências
RUN pip install -r requirements.txt

# Definir a porta
ENV PORT 8501

# Comando para executar a aplicação
CMD ["python", "-m", "streamlit", "run", "app.py"]