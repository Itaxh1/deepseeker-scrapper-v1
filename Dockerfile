# Use the official Streamlit base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy files
COPY main.py secrets.toml ./  
COPY requirements.txt ./  

# Install dependencies
RUN pip install --upgrade pip \
    && pip install streamlit \
    && if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Expose Streamlit default port
EXPOSE 8501

# Start Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
