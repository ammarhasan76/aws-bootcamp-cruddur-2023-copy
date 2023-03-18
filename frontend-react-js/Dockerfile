# Base Image
FROM node:16.18

# Set Env Vars
ENV PORT=3000

# Copy from local filesystem to container
COPY . /frontend-react-js

# Set working directory context
WORKDIR /frontend-react-js

# Install npm in container
RUN npm install

#Expost port defined in the env vars above
EXPOSE ${PORT}

# Command to execute once container is running
CMD ["npm", "start"]