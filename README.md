# ⚡ syspulse

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS EC2](https://img.shields.io/badge/AWS_EC2-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

A lightweight, containerized server monitoring dashboard that tracks CPU, RAM, temperature, and fan speed in real time, featuring historical persistence and automated CI/CD deployment.

## 🏗️ Stack
- **Backend:** Python · Flask · Gunicorn
- **Database:** SQLite (metrics history logging)
- **Containerization:** Docker · Docker Compose (Multi-stage build)
- **Infrastructure:** AWS EC2 (Ubuntu 26.04, ap-south-1) · Nginx (reverse proxy)
- **CI/CD:** GitHub Actions · pytest

## ✨ Features
- **Live Metrics Dashboard:** Polls hardware data every 2 seconds.
- **Secure Access:** API key authentication enforced on all endpoints.
- **Automated Alerts:** Detection thresholds for high CPU/RAM spikes.
- **Background Persistence:** SQLite daemon logging metrics every 30 seconds with a historical view (last 10 readings).
- **Automated Quality Gate:** CI pipeline triggers on every push to `main`, running a test suite before allowing deployment.

## 🚀 Run locally

*(Note: The live AWS EC2 deployment utilizes an ephemeral IP to optimize student compute costs. Please use the instructions below to spin up the containerized architecture in your own local environment).*

```bash
cp .env.example .env
# Edit .env to add your API key

docker compose up --build
# Open http://localhost