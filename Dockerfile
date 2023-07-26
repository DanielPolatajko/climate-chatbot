# Use the official Python image from the Docker Hub
FROM python:3.10

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.5.1

# Create a directory for the application
WORKDIR /app

# Install dependencies (uses the existing pyproject.toml and poetry.lock files)
COPY pyproject.toml poetry.lock ./
RUN curl -sSL https://install.python-poetry.org | python - --version $POETRY_VERSION

RUN /root/.local/bin/poetry config virtualenvs.create false
#    && \
#    /root/.local/bin/poetry install --only main

# Copy the source code into the container
COPY . .

# Set environment variables required by Streamlit
#ENV LC_ALL=C.UTF-8
#ENV LANG=C.UTF-8

# Expose the app port
#EXPOSE 8501

# Run the app
CMD ["/root/.local/bin/poetry", "run", "python", "climate_chatbot/app.py"]
