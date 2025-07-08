
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for mediapipe and opencv
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libfontconfig1 \
    libgl1-mesa-glx \
    libprotobuf-dev \
    protobuf-compiler \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --verbose

# Copy application code
COPY app.py .

# Expose Gradio port
EXPOSE 7860

# Run Gradio app
CMD ["python", "app.py"]
