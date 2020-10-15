# build stage
FROM alpine/git as clone-stage
WORKDIR /app
RUN git clone https://github.com/avsolatorio/dfr-browser.git && mkdir /app/dfr-browser/data

# production stage
FROM nginx:stable-alpine as production-stage

COPY --from=clone-stage /app/dfr-browser /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
