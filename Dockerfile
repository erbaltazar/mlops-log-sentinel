# 1. Use an official lightweight Python image
FROM python:3.11-slim
ENV TZ=Asia/Tokyo

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your script and the log file into the container
# (In a real scenario, we'd 'mount' the log, but let's start simple)
COPY app5.py .
COPY system.log .

# 4. Run the script when the container starts
CMD ["python", "app5.py"]