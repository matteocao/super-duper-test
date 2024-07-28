FROM python:latest

RUN mkdir /data
RUN pip install plotly

ADD dummy/main.py main.py

CMD ["python", "main.py"]
