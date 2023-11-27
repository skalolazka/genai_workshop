FROM ubuntu:22.04

# Install pip
RUN apt-get update && apt-get install -y \
    python3-pip
 
# Create app directory
WORKDIR /app

# Copy files
COPY . .

# Install Python requirements
RUN pip install -r requirements.txt

# Run Flask app
EXPOSE 5000
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]
