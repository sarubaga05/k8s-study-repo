FROM nginx:alpine

COPY index.html /usr/share/nginx/html/
COPY results.html /usr/share/nginx/html/

# Создаем конфиг Nginx для проксирования запросов к backend
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html; \
    } \
    location /results { \
        root /usr/share/nginx/html; \
    } \
    location /api/ { \
        proxy_pass http://backend-service:5000/; \
        proxy_set_header Host $host; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]