FROM python:3.11-slim
WORKDIR /app
# Las dependencias primero: si no cambian, Docker reutiliza esta capa
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]