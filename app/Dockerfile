FROM nvidia/cuda:11.7.1-base-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

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
    python3 python3-pip \
    wget \
    && wget http://ftp.gnu.org/gnu/libc/glibc-2.32.tar.gz \
    && tar -xvzf glibc-2.32.tar.gz \
    && cd glibc-2.32 \
    && mkdir build && cd build \
    && ../configure --prefix=/opt/glibc-2.32 \
    && make -j$(nproc) \
    && make install \
    && cd ../.. \
    && rm -rf glibc-2.32 glibc-2.32.tar.gz \
    && rm -rf /var/lib/apt/lists/*
    
# Ensure the container uses the new glibc version
ENV LD_LIBRARY_PATH=/opt/glibc-2.32/lib:$LD_LIBRARY_PATH

RUN ln -sf /usr/bin/python3 /usr/bin/python

ENV TZ=Europe/Berlin
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

