from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import fastapi.middleware.cors as _cors

app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
]
app.add_middleware(
    _cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginFshare (BaseModel):
    user_email: str
    password: str


class LinkDownload(BaseModel):
    zipflag: int
    url: str
    password: str
    token: str
    session_id: str

#####


@app.post("/loginFshare")
async def login_fshare(item: LoginFshare):
    url = 'https://api.fshare.vn/api/user/login'
    appKey = 'dMnqMMZMUnN5YpvKENaEhdQQ5jxDqddt'
    userAgent = 'macflix-8TY6B8'

    url = 'https://api.fshare.vn/api/user/login'
    headers = {'user-agent': userAgent,
               'content-type': 'application/json'}

    payload = {'user_email': item.user_email,
               'password':	item.password,
               'app_key': appKey}

    r = requests.post(url, data=json.dumps(payload), headers=headers)

    return r.json()


@app.post("/linkDownload")
async def login_fshare(item: LinkDownload):
    headers = {'Cookie': f'session_id={item.session_id}'}

    data = {
        "zipflag": item.zipflag,
        "url": item.url,
        "password": item.password,
        "token": item.token,
    }
    r = requests.post('https://api.fshare.vn/api/session/download',
                      data=json.dumps(data), headers=headers)
    return r.json()
