FROM python:3.12-slim

WORKDIR /app
COPY . .

# The program saves to data/inventory.json, i.e. /app/data/inventory.json.
# Mount a host folder onto /app/data to keep the file after the container stops.
RUN mkdir -p /app/data

CMD ["python", "inventorymanager.py"]
