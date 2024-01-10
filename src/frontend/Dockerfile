FROM node:21-alpine

WORKDIR /app

# Install Node dependencies
COPY package.json ./
RUN npm install --production

# Copy application files
COPY . .

# Run application
CMD ["npm", "run", "build"]

FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]


