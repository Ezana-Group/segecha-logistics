# Deployment Guide

This guide covers the deployment process for the Segecha Logistics platform.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Nginx
- Supervisor
- SSL certificate

## Server Setup

1. Update system packages:
```bash
sudo apt update
sudo apt upgrade
```

2. Install required packages:
```bash
sudo apt install python3-pip python3-venv postgresql nginx supervisor
```

3. Create PostgreSQL database:
```bash
sudo -u postgres psql
CREATE DATABASE segecha_logistics;
CREATE USER segecha WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE segecha_logistics TO segecha;
```

## Application Deployment

1. Clone the repository:
```bash
git clone https://github.com/your-org/segecha_logistics.git
cd segecha_logistics
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize database:
```bash
flask db upgrade
```

## Nginx Configuration

Create a new Nginx configuration file:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /path/to/segecha_logistics/static;
    }
}
```

Enable the configuration:
```bash
sudo ln -s /etc/nginx/sites-available/segecha_logistics /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Supervisor Configuration

Create a new Supervisor configuration file:

```ini
[program:segecha_logistics]
directory=/path/to/segecha_logistics
command=/path/to/segecha_logistics/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/segecha_logistics/err.log
stdout_logfile=/var/log/segecha_logistics/out.log
```

Enable the configuration:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start segecha_logistics
```

## SSL Configuration

1. Install Certbot:
```bash
sudo apt install certbot python3-certbot-nginx
```

2. Obtain SSL certificate:
```bash
sudo certbot --nginx -d your-domain.com
```

## Backup Setup

1. Create backup directory:
```bash
mkdir -p /path/to/backups
```

2. Add backup cron job:
```bash
0 0 * * * /path/to/segecha_logistics/scripts/backup.py
```

## Monitoring

1. Set up logging:
```bash
mkdir -p /var/log/segecha_logistics
chown www-data:www-data /var/log/segecha_logistics
```

2. Configure log rotation:
```bash
sudo nano /etc/logrotate.d/segecha_logistics
```

Add:
```
/var/log/segecha_logistics/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
}
```

## Security Considerations

1. Configure firewall:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

2. Set up fail2ban:
```bash
sudo apt install fail2ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
```

3. Regular security updates:
```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## Maintenance

1. Regular backups:
- Daily automated backups
- Weekly manual backup verification
- Monthly backup restoration test

2. System updates:
- Weekly security updates
- Monthly system updates
- Quarterly dependency updates

3. Monitoring:
- Daily log review
- Weekly performance check
- Monthly security audit

## Troubleshooting

Common issues and solutions:

1. Application not starting:
```bash
sudo supervisorctl status
sudo tail -f /var/log/segecha_logistics/err.log
```

2. Database connection issues:
```bash
sudo -u postgres psql -d segecha_logistics
```

3. Nginx issues:
```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

## Rollback Procedure

1. Stop the application:
```bash
sudo supervisorctl stop segecha_logistics
```

2. Restore from backup:
```bash
./scripts/restore.py --backup-file /path/to/backup.zip
```

3. Restart the application:
```bash
sudo supervisorctl start segecha_logistics
``` 