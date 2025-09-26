FROM node:18-bullseye AS build
WORKDIR /frontend
# Using docker-compose build context at repository root ("..")
COPY frontend/package*.json ./
RUN npm ci || npm install
COPY frontend/ ./
RUN npm run build

FROM nginx:latest
COPY backend/nginx/app.conf /etc/nginx/conf.d/default.conf
COPY --from=build /frontend/build/ /usr/share/nginx/html/
EXPOSE 8000