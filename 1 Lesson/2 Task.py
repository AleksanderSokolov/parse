import requests
import json

key='af2e7a07edcca75efe19649eaefa7144398bff256c8b658b4fc2e9e80ffa254ac252afec6e07c9862a252'
access_token = 'af2e7a07edcca75efe19649eaefa7144398bff256c8b658b4fc2e9e80ffa254ac252afec6e07c9862a252'
token = '533bacf01e11f55b536a565b57531ac114461ae8736d'
url = 'https://api.vk.com/method/users.get?user_ids=210700286&fields=bdate&access_token='+access_token +'&v=5.52'

r = requests.get(url)

def write_json(file_path, text):
    with open(file_path, 'w') as outfile:
        json.dump(text, outfile)
    outfile.close()

print(r.text)
write_json('vk.json', r.text)