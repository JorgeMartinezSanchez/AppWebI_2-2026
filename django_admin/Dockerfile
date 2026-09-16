FROM python:3.11-slim
WORKDIR /django_admin
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "mmy_admin/manage.py", "runserver"]