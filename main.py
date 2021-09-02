from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
app = FastAPI()


class LoginFshare (BaseModel):
    user_email: str
    password: str

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
