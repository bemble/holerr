# Front build
FROM node:20-alpine as front-builder
RUN apk add --no-cache python3 py3-pip make g++

ADD . /app
WORKDIR /app/front
RUN npm ci install
RUN CI=false GENERATE_SOURCEMAP=false npm run build:docker

# Final image
FROM python:3.12-alpine

ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}

# copy front files
COPY --from=front-builder /app/public /app/public

# copy server files
COPY ./server /app/server

WORKDIR /app/server
RUN pip install -r requirements.txt

WORKDIR /app
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 8765