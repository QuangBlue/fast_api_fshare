from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import bs4
from bs4 import BeautifulSoup
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


class FileFshare(BaseModel):
    link: str

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
               'password':  item.password,
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


@app.post("/infoFshare")
async def info_fshare(item: FileFshare):
    url = item.link
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        titleFile = soup.find("div", class_="name").attrs["title"]
        sizeFile = soup.find_all(
            "button", id='download-free')[1].text.strip().split(" | ")[1]
    except:
        return {'msg': 'File does not exist', 'code': 'error'}
    typeFile = titleFile.split(".")[-1]  # mkv
    # Justice.League.Snyders.Cut.2021.1080p.Untouched.HD.AVC.x264
    nameFile = titleFile.split(f'.{typeFile}')[0]

    listRes = ['2160p', '1080p', '720p']
    resFile = 'other'

    for res in listRes:
        r = titleFile.find(res)
        if r != -1:
            resFile = res
            break

    encodeFile = ''
    listEncode = ['hevc', '265']
    listEncode1 = ['avc', '264']

    for q in listEncode:
        r = titleFile.lower().find(q)
        if r != -1:
            encodeFile = 'x265'
            break

    for q1 in listEncode1:
        r = titleFile.lower().find(q1)
        if r != -1:
            encodeFile = 'x264'
            break

    typeAudio = ''
    tAAC = titleFile.lower().find('aac')
    if tAAC != -1:
        typeAudio = 'AAC'

    listAC3 = ['ddp', 'ac3', 'truehd', 'dd']

    for ac3 in listAC3:
        r = titleFile.lower().find(ac3)
        if r != -1:
            typeAudio = 'AC-3'
            break
    tDts = titleFile.lower().find('dts')
    if tDts != -1:
        typeAudio = 'DTS'

    qualityFile = ''
    listQuality = ['bluray', 'blu-ray']
    for x in listQuality:
        qBr = titleFile.lower().find(x)
        if qBr != -1:
            qualityFile = 'BR Encode'
    qBr1 = titleFile.lower().find('remux')
    if qBr1 != -1:
        qualityFile = 'BR Remux'

    listQ3 = ['web-dl', 'hdtv', 'webrip']
    for x in listQ3:
        qqq = titleFile.lower().find(x)
        if qqq != -1:
            qualityFile = x.upper()
            break
    channelFile = ''
    listChannel = ['5.1', '7.1']
    for x in listChannel:
        qqq = titleFile.lower().find(x)
        if qqq != -1:
            channelFile = x
            break
    hdrFile = ''
    hdr = titleFile.lower().find('hdr')
    if hdr != -1:
        hdrFile = 'HDR'

    if typeFile == 'iso':
        resFile = 'ISO'

    json = {
        'msg': 'File is exist',
        'code': 'success',
        'name': nameFile,
        'type': typeFile,
        'size': sizeFile,
        'resolution': resFile,
        'encode_type': encodeFile,
        'audio_type': typeAudio,
        'quality': qualityFile,
        'audio_channel': channelFile,
        'hdr': hdrFile,
    }

    return json
