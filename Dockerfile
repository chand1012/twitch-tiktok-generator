FROM python:3.10-alpine

# Install system dependencies
RUN apk add --update --no-cache \
    ffmpeg

# Upgrade pip and install pipenv
RUN pip install --upgrade pip && \
    pip install --no-cache-dir pipenv

# Copy local directory into container
WORKDIR /app
COPY . /app

# Install production dependencies from Pipfile
RUN pipenv install --system --deploy --ignore-pipfile

# Set the entrypoint
ENTRYPOINT ["python", "gen.py", "generate"]
