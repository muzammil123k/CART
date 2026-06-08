# 1. Use the official, lightweight Python Linux operating system
FROM python:3.11-slim

# 2. Tell Docker where we are going to work inside the container
WORKDIR /app

# 3. Copy ONLY the requirements first (this makes future builds lightning fast)
COPY requirements.txt .

# 4. Install the exact dependencies from your laptop
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your actual code into the container
COPY . .

# 6. Expose the port so the outside world can talk to FastAPI
EXPOSE 8000

# 7. The exact command the server runs when it wakes up
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]