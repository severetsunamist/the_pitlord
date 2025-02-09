# Use an official Python runtime as a parent image
FROM python:3.12.3-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Set the working directory
WORKDIR /webapp

# Copy only the dependency files first to leverage Docker layer caching
COPY pyproject.toml poetry.lock ./

# Install Poetry and dependencies
# Install dependencies and Poetry
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -sSL https://install.python-poetry.org | python3 - --yes

# Update PATH globally to include Poetry's bin directory
ENV PATH="/root/.local/bin:$PATH"

# Configure Poetry and install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code
COPY ./webapp /webapp

# Expose the port
EXPOSE 8080

# # Run the application
# CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && gunicorn webapp.wsgi:application --bind 0.0.0.0:${PORT}"]