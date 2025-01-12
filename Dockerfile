# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install dependencies
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


# Expose the port that Flask runs on
EXPOSE 5000

# Run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:$PORT", "app:app"]
