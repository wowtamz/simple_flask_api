FROM runpod/gpt4all

# Ensure no GPU support
#ENV CUDA_VISIBLE_DEVICES=""

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

