FROM python:3.10.21-alpine3.24


RUN pip install flask 

COPY config/ /site_config/

EXPOSE 5000

CMD ["python3", "/site_config/main.py"]