#!/bin/bash

uvicorn soi_proxy_launch:app --port 5520 --host 0.0.0.0 --reload --log-level error --root-path /soiproxy

conf="
nano /etc/apache2/sites-available/server.nikhilvj.co.in-le-ssl.conf

    ProxyPass /soiproxy/ http://127.0.0.1:5520/
    ProxyPassReverse /soiproxy/ http://127.0.0.1:5520/

systemctl reload apache2
"
