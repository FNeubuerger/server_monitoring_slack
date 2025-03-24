# Use official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy files to the container
COPY server_status_bot.py . 
# Copy the secrets file to the container
COPY secrets.json .
# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt

# Run the script
CMD ["python", "server_status_bot.py"]