FROM python:3.8-buster

RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/avanan

#COPY avanan/requirements.txt /opt/app/avanan
COPY avanan /opt/app/avanan


WORKDIR /opt/app/avanan
RUN pip install -r requirements.txt


EXPOSE 8000
CMD ["python", "manage.py",  "runserver", "0.0.0.0:8000"]
