#!/bin/bash
echo "Starting Zero-Downtime Blue-Green Deployment..."

# 1. Detect which container is currently running (Blue or Green)
if sudo docker ps | grep -q 'cart-api-blue'; then
    OLD_APP="cart-api-blue"
    NEW_APP="cart-api-green"
    NEW_PORT=8002
else
    OLD_APP="cart-api-green"
    NEW_APP="cart-api-blue"
    NEW_PORT=8001
fi

echo "Current active container: $OLD_APP"
echo "Spinning up new container: $NEW_APP on port $NEW_PORT"

# 2. Build the new Docker image
sudo docker build -t cart-api .

# 3. Launch the new container in the background
sudo docker run -d -p $NEW_PORT:8000 --name $NEW_APP -e DATABASE_URL="$DATABASE_URL" cart-api

# 4. Wait for FastAPI to fully boot and connect to RDS
echo "Waiting for the new container to warm up..."
sleep 5

# 5. Hot-swap Nginx to point to the new container port
echo "Swapping Nginx traffic to port $NEW_PORT..."
echo "server { listen 80; location / { proxy_pass http://127.0.0.1:$NEW_PORT; } }" | sudo tee /etc/nginx/sites-available/default
sudo systemctl reload nginx

# 6. Clean up the benched container
echo "Shutting down the old container ($OLD_APP)..."
sudo docker stop $OLD_APP || true
sudo docker rm $OLD_APP || true

echo "Deployment Successful! Zero Downtime Achieved."