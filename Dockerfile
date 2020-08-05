FROM node:12 AS web_builder

WORKDIR /app/web_frontend
ADD ./web_frontend /app/web_frontend
RUN npm install
RUN npm build
RUN npm audit fix

FROM python:3.8

WORKDIR /app
ADD ./requirements.txt /app
ADD ./tba_engine /app
COPY --from=web_builder /app/web_frontend/build /app/web_frontend/build
RUN pip install -r requirements.txt

CMD ["gunicorn", "server:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0"]

