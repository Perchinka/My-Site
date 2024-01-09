FROM node:21-alpine

WORKDIR /app

# Install Node dependencies
COPY package.json ./
RUN npm install

# Copy application files
COPY ./ /app

# Run application
CMD ["npm", "run", "start"]

