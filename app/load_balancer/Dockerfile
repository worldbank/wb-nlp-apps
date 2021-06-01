# production stage
FROM nginx:stable-alpine as production-stage
COPY nginx.conf /etc/nginx/nginx.conf
COPY site.conf /etc/nginx/conf.d/site.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
