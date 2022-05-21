## SOI PNG proxy

API Doc (swagger): http://localhost:5520/docs

Can test the tile URL quickly on https://geojson.io (Meta -> Add map layer)

On local:  
http://localhost:5520/{z}/{x}/{y}.png  

Live:  
https://server.nikhilvj.co.in/soiproxy/{z}/{x}/{y}.png  

Example:  
https://server.nikhilvj.co.in/soiproxy/15/23460/14023.png  


Started on 21 May 2022 by Nikhil VJ, https://nikhilvj.co.in

Aim : serve a proxy map tiles URL that takes webp tiles from: https://storage.googleapis.com/soi_data/export/tiles/{z}/{x}/{y}.webp tileURL setup by https://github.com/ramSeraph/ .

With code from:  
https://github.com/ramSeraph/opendata/blob/master/maps/SOI/webp_to_png.py


Fetches orig webp tile, converts to png and returns tile

