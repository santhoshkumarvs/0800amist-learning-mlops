# Base Image for Building ML App
FROM python

# Working Directory
WORKDIR /mlapp

# Copy Requriments.txt and app.py, and data/rental_1000.csv
COPY . .

# Libarires to installed
RUN pip install --no-cache-dir -r requirements.txt

# Expose Port 5000
EXPOSE 5000

# Default Commands to run at start of Container
CMD ["python","mlapp.py" ]

# Dockerfile was written by Siddarth