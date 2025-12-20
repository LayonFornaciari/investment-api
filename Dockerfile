FROM python:3.11-slim

# Evita arquivos .pyc e buffer de log
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto
COPY . .

# Expõe a porta
EXPOSE 8000

# Roda a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]