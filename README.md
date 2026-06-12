# syspulse

A lightweight server monitoring dashboard that tracks CPU, RAM, 
temperature and fan speed in real time, with historical logging via SQLite.

## Stack
- Python · Flask · Gunicorn
- SQLite (metrics history logging)
- Docker · Docker Compose
- Nginx (reverse proxy)
- AWS EC2 (Ubuntu 26.04, ap-south-1)

## Features
- Live metrics dashboard (polls every 2s)
- API key authentication on all endpoints
- Alert detection for high CPU/RAM
- SQLite background logging every 30s
- Historical metrics view (last 10 readings)
- Multi-stage Docker build

## Live Demo
http://3.111.53.205

## Run locally
cp .env.example .env
docker compose up --build
# Open http://localhost
