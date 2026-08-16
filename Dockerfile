FROM python:3.10.21-alpine3.24

# only for ubuntu or debian based images

# RUN apt-get update && apt-get install -y nano
# RUN apt-get install -y python3 python3-pip
RUN pip install flask 

COPY config/ /site_config/

VOLUME /site_config

EXPOSE 5000

CMD ["python3", "/site_config/main.py"]