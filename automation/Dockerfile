FROM python:3.9-slim

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libgtk-3-0 \
    libasound2 \
    libnss3 \
    libxss1 \
    libxtst6 \
    libwayland-client0 \
    libwayland-cursor0 \
    libwayland-egl1 \
    libxkbcommon0 \
    curl \
    && apt-get clean

# Upgrade pip, install Playwright, and install Chromium
RUN pip install --upgrade pip && \
    pip install playwright && \
    playwright install chromium

# Set working directory
WORKDIR /app

# Copy your code into container
COPY . .

# Run scraper + log output + keep container alive
CMD ["bash", "-c", "python3 hhs_daily_articles.py >> automation.log 2>&1 && tail -f automation.log"]
