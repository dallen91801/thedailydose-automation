FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv git curl vim build-essential \
    && apt-get clean

# Set up virtual environment
RUN python3 -m venv /opt/ai_stack
ENV PATH="/opt/ai_stack/bin:$PATH"

# Upgrade pip and install core Python packages
RUN pip install --upgrade pip && \
    pip install \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 && \
    pip install \
    tensorflow \
    transformers \
    newspaper3k \
    requests \
    beautifulsoup4


WORKDIR /app

# Don't copy — the volume mount handles this
# COPY . /app

CMD [ "bash" ]
