FROM python:3.11-slim

# Set the operational directory inside the container
WORKDIR /app

# Install standard gcc toolchain
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc && rm -rf /var/lib/apt/lists/*

# Copy dependency mappings
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy all project backend files
COPY . .

# Expose Render's default port (10000)
EXPOSE 10000

# Forces Python to flush output directly to Render logs
ENV PYTHONUNBUFFERED=1

# Execute through Python's module path for maximum stability
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]