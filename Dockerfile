FROM python:3.8-slim-buster
WORKDIR /app
COPY . /app

# Update the package lists and install awscli
RUN apt-get update -y && apt-get install -y awscli


# Install other dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    unzip && \
    pip install -r requirements.txt
CMD ["python3", "application.py"]
