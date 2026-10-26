FROM python:3.12-slim
WORKDIR /app
COPY api ./api
COPY ui ./ui
COPY openapi.json .
CMD ["python", "api/server.py", "--host", "0.0.0.0"]
