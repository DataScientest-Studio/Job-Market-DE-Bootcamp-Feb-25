# 2_data_consumption/streamlit_viz/Dockerfile
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy app code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir \
    streamlit \
    pandas \
    requests \
    numpy \
    matplotlib \
    seaborn

# Expose port Streamlit runs on
EXPOSE 8501

# Start the Streamlit app
CMD ["streamlit", "run", "fastapi_viz.py", "--server.port=8501", "--server.address=0.0.0.0"]