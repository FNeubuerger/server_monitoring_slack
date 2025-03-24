# Use official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy files to the container
COPY server_status_bot.py . 
# Copy the secrets file to the container
COPY secrets.json .

# Install dependencies
RUN pip install psutil slack-sdk gputil requests

# Run the script
CMD ["python", "server_status_bot.py"]