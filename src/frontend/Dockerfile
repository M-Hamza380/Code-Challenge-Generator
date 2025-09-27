# Stage 1: Build stage
FROM node:24.5.0-slim AS build

WORKDIR /app

COPY package.json \ package-lock.json ./
COPY .env vite.config.js eslint.config.js ./
RUN npm ci

COPY index.html ./
COPY src ./src
COPY public ./public
RUN npm run build

# Stage 2: Production stage
FROM node:24.5.0-slim

WORKDIR /app

COPY --from=build /app/dist ./dist
COPY --from=build /app/package.json ./
COPY --from=build /app/package-lock.json ./

RUN npm install

EXPOSE 4173

CMD [ "npm", "run", "preview", "--", "--host" ]

