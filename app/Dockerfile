FROM nvidia/cuda:11.7.1-base-ubuntu20.04

#python:3.11

# Ensure no GPU support
#ENV CUDA_VISIBLE_DEVICES=""

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

