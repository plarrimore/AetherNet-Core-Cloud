FROM python:3.11-slim

# Set the operational directory inside the container
WORKDIR /app

# Install standard compiler tools
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc && rm -rf /var/lib/apt/lists/*

# Copy dependency mappings
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy all project backend files sitting in the context folder
COPY . .

# Forces Python to flush standard output streams immediately to Render logs
ENV PYTHONUNBUFFERED=1

# Execute directly via Python's native runtime entrypoint
CMD ["python", "main.py"]