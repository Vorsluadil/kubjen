# Используем официальный образ Nginx в качестве базы
FROM nginx:latest

# Копируем наш файл конфигурации в контейнер
COPY default.conf /etc/nginx/conf.d/default.conf

# Открываем порт 80 (необязательно, но удобно для документации)
EXPOSE 80

# Запускаем Nginx в режиме "переднего плана"
CMD ["nginx", "-g", "daemon off;"]
