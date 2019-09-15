import requests
import json

token = 'ace8ed39fe714cfd0bebb690a6bc03d0a0caa40b'
url = 'https://api.github.com/user/repos'

head = {'Authorization': 'token {}'.format(token)}
r = requests.get(url, headers=head)

def write_json(file_path, text):
    with open(file_path, 'w') as outfile:
        json.dump(text, outfile)
    outfile.close()

print(r.text)
write_json('gh.json', r.text)
