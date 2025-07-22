# Use official Python slim base
FROM python:3.11-slim

WORKDIR /app

# Copy your app code
COPY main.py requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Streamlit (default 8501)
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.headless=true"]
