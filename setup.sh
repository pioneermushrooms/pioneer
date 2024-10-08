#!/bin/bash

# Install Apache and necessary modules
sudo yum install httpd -y
sudo yum install mod_proxy mod_proxy_http -y

# Install conda if not already installed
# (You may need to add this part depending on the machine)

# Set up the Conda environment
conda create --name myenv python=3.9 -y
conda activate myenv

# Install Python dependencies
pip install -r /path/to/dataquiz/requirements.txt

# Start Gunicorn
gunicorn --workers 3 --bind 0.0.0.0:8000 dataquiz:app --access-logfile gunicorn-access.log --error-logfile gunicorn-error.log &

# Configure Apache to proxy requests
echo "
<VirtualHost *:80>
    ServerName your-server-ip-or-domain
    DocumentRoot /path/to/dataquiz

    <Directory /path/to/dataquiz>
        Require all granted
        Options FollowSymLinks
        AllowOverride None
    </Directory>

    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>
" | sudo tee /etc/httpd/conf.d/dataquiz.conf

# Restart Apache
sudo systemctl restart httpd

