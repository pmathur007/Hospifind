
#!/bin/bash
cd /home/ubuntu/hospifind
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" |xargs rm -rf
sudo pkill -f uwsgi -9
sudo pkill -f nginx -9
sudo systemctl restart uwsgi
sudo systemctl restart nginx
sudo systemctl restart hospifind
sudo systemctl start hospifind
sudo systemctl enable hospifind
echo "All Services Restarted (nginx, uwsgi, flask)"
