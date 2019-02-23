FROM python:3.7-stretch


COPY . /backend
WORKDIR /backend

RUN pip install -r requirements/prod.txt

EXPOSE 8088

ENTRYPOINT ["python3", "run.py"]