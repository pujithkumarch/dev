# Use the official lightweight Nginx image
FROM nginx:alpine

# Copy a custom index.html to the Nginx server (Optional, but good for testing)
RUN echo "<h1>Hello from my EKS Cluster!</h1>" > /usr/share/nginx/html/index.html

# Expose port 80
EXPOSE 80
