FROM python:3.9-slim

# Ensure no GPU support
#ENV CUDA_VISIBLE_DEVICES=""

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN sudo apt-get install -y libcudart11

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

