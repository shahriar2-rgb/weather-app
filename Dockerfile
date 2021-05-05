FROM python:3.6.1-alpine
WORKDIR /usr/src/temperature_website_flask
COPY . .
RUN pip install -r requirements.txt
CMD ["python","app.py"]