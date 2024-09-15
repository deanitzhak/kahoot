# Use a Node.js image
FROM node:16-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./

RUN npm install

# Copy the entire app to the container
COPY . .

# Build the Svelte app for production
RUN npm run build

# Use a simple Node.js HTTP server for serving the built app
RUN npm install -g serve

# Expose port 5003
EXPOSE 5003

# Serve the app
CMD ["serve", "-s", "public", "-l", "5003"]
