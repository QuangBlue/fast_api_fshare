import requests

# url = 'https://api.fshare.vn/api/user/login'
# headers = {'user-agent': 'macflix-8TY6B8',
#            'content-type': 'application/json'}

# payload = {'user_email': 'quanglynguyen1603@gmail.com',
#            'password':	'Khamy123!@#',
#            'app_key': 'dMnqMMZMUnN5YpvKENaEhdQQ5jxDqddt'}

# r = requests.post(url, headers=headers, payload=payload)

# print(r.text)

import json

url = 'https://api.fshare.vn/api/user/login'
headers = {'user-agent': 'macflix-8TY6B8',
           'content-type': 'application/json'}

payload = {'user_email': 'quanglynguyen1603@gmail.com',
           'password':	'Khamy123!@#',
           'app_key': 'dMnqMMZMUnN5YpvKENaEhdQQ5jxDqddt'}

r = requests.post(url, data=json.dumps(payload), headers=headers)

print(r.text)
