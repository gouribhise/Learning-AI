import requests

url="https://dog.ceo/api/breeds/image/random"
response=requests.get(url)
if response.status_code==200:
    data=response.json()
    print(data["message"])