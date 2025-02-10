# Use an official Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy your app files into the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the app
CMD ["python", "app2.py"]
