FROM python:3.10-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY ./inmuebles /code/inmuebles

ENV PYTHONPATH=/code/inmuebles/

CMD ["uvicorn", "inmuebles.main:inmuebles", "--host", "0.0.0.0", "--port", "80"]