FROM python:3.11-slim

WORKDIR /post-creation-service

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run/Functions will send traffic to port 8080
ENV PORT=8080

# 👇 Run the Functions Framework instead of python app.py
CMD ["functions-framework", "--target=main", "--port=8080"]
