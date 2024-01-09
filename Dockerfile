# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

# Install system dependencies required for network diagnostics and Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg2 \
    iputils-ping \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright
RUN playwright install
RUN playwright install-deps

# Now copy the rest of the application's source code
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run your application command when the container launches
CMD ["python", "-m", "app"]
