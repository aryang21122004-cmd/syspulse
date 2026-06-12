# syspulse

A lightweight server monitoring dashboard that tracks CPU, RAM, temperature, and fan speed in real time.

## Stack
- Python · Flask · Gunicorn
- Docker · Docker Compose
- Nginx (reverse proxy)
- AWS EC2 (Ubuntu 22.04)

## Features
- Live metrics dashboard (polls every 3s)
- API key authentication
- Alert detection for high CPU/RAM
- Containerised with multi-stage Docker build

## Run locally
cp .env.example .env   # set your API_KEY
docker compose up --build
# Open http://localhost

## Live Demo
http://3.111.53.205
