FROM python:3.9-slim
# Set working directory (créer un dossier app dans le docker)
WORKDIR /app

# Copy package code
COPY . .

# Install libraries
# COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install  -r requirements.txt


#CMD [ "python", "app/main.py" ]