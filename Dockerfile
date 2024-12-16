# FROM python:3.10
FROM apache/spark-py:v3.4.0

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port
EXPOSE 8080

# Run the command to start the application
CMD ["spark-submit", "--jars", "/app/jars/postgresql-42.7.4.jar", "/app/app.py"]