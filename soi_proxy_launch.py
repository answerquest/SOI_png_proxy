# soi_proxy_launch.py
# Started on 21 May 2022 by Nikhil VJ, https://nikhilvj.co.in
# aim : serve a proxy map tiles URL that takes webp tiles from:
# https://storage.googleapis.com/soi_data/export/tiles/{z}/{x}/{y}.webp
# fetches orig webp tile, converts to png and returns tile

CACHE_DAYS = 365

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # https://fastapi.tiangolo.com/tutorial/cors/
from fastapi.responses import StreamingResponse # for binary data response
from fastapi import HTTPException
# from fastapi.staticfiles import StaticFiles # static html files deploying

# for webp to png conversion, from https://github.com/ramSeraph/opendata/blob/master/maps/SOI/webp_to_png.py
import io, requests
from PIL import Image

app = FastAPI()

# allow cors - from https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Static content - might use this 
# https://fastapi.tiangolo.com/tutorial/static-files/
# app.mount("/gpx", StaticFiles(directory="gpx", html = False), name="static2")


@app.get("/{z}/{x}/{y}.png", tags=["tiles"])
def webp2png(z:int, x:int, y:int):
    # sample: https://storage.googleapis.com/soi_data/export/tiles/15/23460/14022.webp
    
    # handle invalid requests without bothering to hit the orig server,
    # like: https://server.nikhilvj.co.in/soiproxy/17/92954/58146.png
    if z > 15 or z <4:
        raise HTTPException(status_code=406)

    url = f"https://storage.googleapis.com/soi_data/export/tiles/{z}/{x}/{y}.webp"
    r = requests.get(url)
    
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code)

    # https://github.com/ramSeraph/opendata/blob/master/maps/SOI/webp_to_png.py
    # returning an image, https://stackoverflow.com/a/70625157/4355695

    inp_f = io.BytesIO(r.content)
    img = Image.open(inp_f, formats=('WEBP',))
    imgio = io.BytesIO()
    # img.save(imgio, format='PNG', params={'optimize': True})
    img.save(imgio, format='PNG', compress_level=1)
    # using min compression level to have min processing time. https://github.com/python-pillow/Pillow/issues/1211#issuecomment-98800656 
    imgio.seek(0)

    response = StreamingResponse(content=imgio, media_type="image/png")

    # adding cache headers so that if client side is revisiting same places, don't bug us anymore.
    # how to set header in response: https://stackoverflow.com/questions/61140398/fastapi-return-a-file-response-with-the-output-of-a-sql-query#61910803
    # cache header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
    global CACHE_DAYS
    response.headers['Cache-Control'] = f"max-age={CACHE_DAYS*24*3600}"

    return response


@app.get("/{z}/{x}/{y}.webp", tags=["tiles"])
def proxywebp(z:int, x:int, y:int):
    # handle invalid requests without bothering to hit the orig server,
    # like: https://server.nikhilvj.co.in/soiproxy/17/92954/58146.png
    if z > 15 or z <4:
        raise HTTPException(status_code=406)
    url = f"https://storage.googleapis.com/soi_data/export/tiles/{z}/{x}/{y}.webp"
    r = requests.get(url)
    inp_f = io.BytesIO(r.content)
    response = StreamingResponse(content=inp_f, media_type="image/webp")
    global CACHE_DAYS
    response.headers['Cache-Control'] = f"max-age={CACHE_DAYS*24*3600}"

    return response