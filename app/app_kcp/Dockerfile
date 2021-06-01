# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
COPY src/config.prod.js ./src/config.js
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY --from=build-stage /app/404.html /usr/share/nginx/html/404.html
COPY --from=build-stage /app/nginx.conf /etc/nginx/nginx.conf
COPY --from=build-stage /app/site.conf /etc/nginx/conf.d/site.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
