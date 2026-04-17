# Minor Project: Deploy Student Grade Tracker on AWS EC2

## Project Overview
A Flask web application that allows adding, viewing, and deleting student grade records. Deployed on AWS EC2 with Nginx as a reverse proxy and Gunicorn as the WSGI server.

---

## Project File Structure

```
student-app/
├── app.py                  ← Flask application (main backend)
├── requirements.txt        ← Python dependencies
├── gunicorn.conf.py        ← Gunicorn production server config
├── Dockerfile              ← Optional Docker containerization
├── studentapp.service      ← Systemd service (auto-start on reboot)
├── nginx_studentapp.conf   ← Nginx reverse proxy config
└── templates/
    └── index.html          ← Frontend HTML template
```

---

## Step 1 — Run Locally (Test Before Deploying)

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open browser: http://localhost:5000
```

---

## Step 2 — Push Code to GitHub

```bash
# Initialize git repo
git init
git add .
git commit -m "Initial commit - Student Grade Tracker"

# Create a repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/student-app.git
git push -u origin main
```

---

## Step 3 — Create AWS EC2 Instance

1. Log in to https://aws.amazon.com/console
2. Go to **EC2 → Launch Instance**
3. Settings:
   - Name: `student-app-server`
   - AMI: **Ubuntu Server 22.04 LTS** (Free Tier eligible)
   - Instance type: **t2.micro** (Free Tier)
   - Key pair: Create new → download `.pem` file (keep it safe!)
4. Security Group — Add inbound rules:
   - SSH (port 22) — Your IP
   - HTTP (port 80) — Anywhere (0.0.0.0/0)
   - Custom TCP (port 5000) — Anywhere (for testing)
5. Click **Launch Instance**
6. Note your **Public IPv4 address**

---

## Step 4 — Connect to EC2 via SSH

```bash
# On your local machine terminal:
chmod 400 your-key.pem

ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

---

## Step 5 — Set Up the Server (Run Inside EC2)

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Python, pip, nginx, git
sudo apt install python3 python3-pip python3-venv nginx git -y
```

---

## Step 6 — Clone and Install Your App

```bash
# Clone from GitHub
git clone https://github.com/YOUR_USERNAME/student-app.git
cd student-app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 7 — Test the App on EC2

```bash
# Run temporarily to test
python app.py

# Visit: http://YOUR_EC2_PUBLIC_IP:5000
# (Press Ctrl+C to stop after testing)
```

---

## Step 8 — Run with Gunicorn (Production Server)

```bash
# Still inside the venv, from student-app directory:
gunicorn -c gunicorn.conf.py app:app

# Test: http://YOUR_EC2_PUBLIC_IP:5000
# (Press Ctrl+C to stop)
```

---

## Step 9 — Set Up Systemd (Auto-Start on Reboot)

```bash
# Copy the service file
sudo cp studentapp.service /etc/systemd/system/

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable studentapp
sudo systemctl start studentapp

# Check status
sudo systemctl status studentapp
```

---

## Step 10 — Configure Nginx (Reverse Proxy on Port 80)

```bash
# Edit the nginx config to replace YOUR_EC2_PUBLIC_IP
nano nginx_studentapp.conf
# Replace YOUR_EC2_PUBLIC_IP with your actual IP

# Copy config
sudo cp nginx_studentapp.conf /etc/nginx/sites-available/studentapp
sudo ln -s /etc/nginx/sites-available/studentapp /etc/nginx/sites-enabled/
sudo nginx -t            # Test config
sudo systemctl restart nginx
sudo systemctl enable nginx
```

Now visit: **http://YOUR_EC2_PUBLIC_IP** (no port number needed!)

---

## Step 11 — Add SSL Certificate (HTTPS) with Let's Encrypt

> Only needed if you have a domain name pointed to your EC2 IP.

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com

# Follow prompts, certbot auto-configures HTTPS
# App now accessible at: https://yourdomain.com
```

---

## Step 12 — Monitor Logs and Performance

```bash
# View app logs
sudo journalctl -u studentapp -f

# View nginx access logs
sudo tail -f /var/log/nginx/access.log

# View nginx error logs
sudo tail -f /var/log/nginx/error.log

# Monitor server resources
htop
```

---

## Optional: Docker Deployment

```bash
# Build the image
docker build -t student-app .

# Run the container
docker run -d -p 5000:5000 --name student-app student-app

# Check running containers
docker ps
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Port 5000 not accessible | Check EC2 Security Group — allow TCP 5000 |
| Nginx 502 Bad Gateway | Make sure gunicorn service is running: `sudo systemctl status studentapp` |
| Permission denied on .pem | Run: `chmod 400 your-key.pem` |
| App not starting | Check logs: `sudo journalctl -u studentapp -n 50` |
| Changes not reflected | Restart service: `sudo systemctl restart studentapp` |

---

## Summary of What Was Used

| Component | Technology |
|---|---|
| Backend | Python Flask |
| Production server | Gunicorn |
| Reverse proxy | Nginx |
| Cloud platform | AWS EC2 (Ubuntu) |
| Version control | Git + GitHub |
| Optional | Docker |
| SSL | Let's Encrypt / Certbot |
