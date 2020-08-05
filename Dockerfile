FROM python:3.8

Add . /app

WORKDIR /app/web_frontend
RUN npm install
RUN npm build

WORKDIR /app
RUN pip install -r requirements.txt

CMD ["gunicorn", "server:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0"]

