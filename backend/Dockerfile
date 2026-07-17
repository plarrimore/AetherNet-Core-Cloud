FROM python:3.11-slim

# Set the operational directory inside the container
WORKDIR /app

# Install basic system binaries required for compiling python modules
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy your dependency map first to leverage caching layers
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy all the files directly from your local backend/ folder into the container's /app/ folder
COPY . .

# Expose the API gateway port
EXPOSE 8000

# Execute the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]