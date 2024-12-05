def get_content():
    return """version: '3.8'

services:
  toctoc_medoc:
    build: .
    container_name: toctocmedoc_preprod_container
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - /home/debian/certificat_ssl/Certifs:/etc/docker/certs:ro
    command: python3 main.py
    depends_on:
      - db    
  db:
    image: postgres:15.3-bullseye
    container_name: postgres_container
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: root
      POSTGRES_DB: toctocmedoc_db
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
"""