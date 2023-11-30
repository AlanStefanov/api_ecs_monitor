FROM python:3.11

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    # Lista de tus paquetes aquí \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt


# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port that the app will run on
EXPOSE 8000

# Apply database migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Run the application
CMD ["gunicorn", "ecs_project.wsgi:application", "--bind", "0.0.0.0:8000"]
