FROM python:3.9

# Install dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

# Copy application files
COPY . /app

# Expose FastAPI default port
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


