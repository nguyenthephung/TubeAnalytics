FROM python:3.13-slim

WORKDIR /app

# Install system dependencies for Python 3.13
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.fastapi.index:app", "--host", "0.0.0.0", "--port", "8000"]