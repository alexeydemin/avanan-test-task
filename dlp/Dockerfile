FROM python:3.8-buster

RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/dlp

COPY dlp /opt/app/dlp


WORKDIR /opt/app/dlp
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
