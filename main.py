import requests
import flask

URL = "https://zcctmart.zendesk.com/api/v2/tickets"
Auth = ('#####', '#####')
# Softcode username and password by entry
re = requests.get(url=URL, auth=Auth)

data = re.json()

for i in data["tickets"]:
    print(i["subject"])