# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy only requirements first (improves build caching)
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt \
    && pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Copy the rest of the application files
COPY . .

# Expose the application port
EXPOSE 8000

# Define the command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
