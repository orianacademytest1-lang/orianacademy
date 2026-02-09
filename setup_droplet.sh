#!/bin/bash
# ====================================================
# Oriana Academy - DigitalOcean Droplet Setup Script
# Run this script on your Droplet after uploading code
# Usage: chmod +x setup_droplet.sh && ./setup_droplet.sh
# ====================================================

set -e  # Exit on any error

echo "🚀 Starting Oriana Academy Server Setup..."

# Step 1: System Update
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Step 2: Install Dependencies
echo "📦 Installing Python, Nginx, and build tools..."
sudo apt install -y python3-pip python3-venv nginx build-essential

# Step 3: Create app directory if not exists
APP_DIR="/var/www/oriana"
if [ ! -d "$APP_DIR" ]; then
    echo "📁 Creating app directory at $APP_DIR..."
    sudo mkdir -p $APP_DIR
fi

# Step 4: Copy current directory to app location (if running from uploaded folder)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "$SCRIPT_DIR" != "$APP_DIR" ]; then
    echo "📁 Copying files to $APP_DIR..."
    sudo cp -r "$SCRIPT_DIR"/* $APP_DIR/
fi

cd $APP_DIR

# Step 5: Setup Python Virtual Environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 6: Install Python Dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r backend/requirements.txt
pip install gunicorn uvicorn

# Step 7: Create Systemd Service
echo "⚙️  Creating systemd service..."
sudo tee /etc/systemd/system/oriana.service > /dev/null <<EOF
[Unit]
Description=Gunicorn instance to serve Oriana Academy
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/oriana
Environment="PATH=/var/www/oriana/venv/bin"
EnvironmentFile=/var/www/oriana/backend/.env
ExecStart=/var/www/oriana/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000 backend.app_local:app

[Install]
WantedBy=multi-user.target
EOF

# Step 8: Start and Enable Service
echo "🔄 Starting Oriana service..."
sudo systemctl daemon-reload
sudo systemctl start oriana
sudo systemctl enable oriana

# Step 9: Configure Nginx
echo "🌐 Configuring Nginx reverse proxy..."
sudo tee /etc/nginx/sites-available/oriana > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/oriana /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

# Step 10: Open Firewall
echo "🔥 Configuring firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw --force enable

echo ""
echo "✅ ======================================"
echo "✅  SETUP COMPLETE!"
echo "✅ ======================================"
echo ""
echo "Your site is now live at: http://$(curl -s ifconfig.me)"
echo ""
echo "Next steps:"
echo "  1. Point your domain to this IP"
echo "  2. Run: sudo certbot --nginx (for HTTPS)"
echo ""
