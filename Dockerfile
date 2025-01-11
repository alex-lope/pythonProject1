# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy essential application files
COPY app.py /app/
COPY requirements.txt /app/
COPY templates /app/templates/
COPY utils /app/utils/
COPY models /app/models/
COPY reports /app/reports/

# Install dependencies
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask runs on
EXPOSE 5000

# Run the application
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]

