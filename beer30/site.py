from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from hypercorn.config import Config
from hypercorn.asyncio import serve
import random
import string

from .light import Light

class Site:
    def __init__(self, light: Light, port: int = 8080, password=None, random_pw_length: int=8):
        self._light = light
        if password == None:
            password = ''.join(random.choice(string.ascii_lowercase) for i in range(random_pw_length))
        self._password = password
        self._port = port

        app = FastAPI()
        app.mount('/static', StaticFiles(directory = 'static'), name = 'static')

        @app.get('/', response_class = HTMLResponse)
        async def index():
            return f"<!DOCTYPE html><html><head><title>Beer30 Light</title></head><body style='background: black; text-align: center;'><img alt='{self._light.state} light' src='/static/{self._light.state}.svg' /></body></html>"

        @app.get('/health')
        async def health():
            return { 'status': 'OK' }

        @app.get('/set')
        async def set_from_params(state: str):
            return set_from_uri(state)

        @app.get('/set/{state}')
        async def set_from_uri(state: str, password: str = None):
            if password == None:
                raise HTTPException(status_code=403, detail='no password provided')
            elif password != self._password:
                raise HTTPException(status_code=403, detail='invalid password')

            if state not in self._light.STATES:
                raise HTTPException(status_code=400, detail=f"bad state provided, valid choices: {','.join(self._light.STATES)}")

            previous_state = self._light.state
            self._light.state = state
            return {'result': 'success', 'state': self._light.state, 'previous': previous_state}

        @app.get('/state')
        async def state():
            return {'state': self._light.state}

        self._app = app

    async def start(self):
        config = Config()
        config.bind = [f'0.0.0.0:{self._port}']

        await serve(self._app, config)