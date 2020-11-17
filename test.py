import requests

BASE="http://127.0.0.1:5000/"

data = [{"name": "Speed", "likes": 10, "views": 100}, 
    {"name": "Top Gun", "likes": 0, "views": 10},
    {"name": "Ice Age", "likes": 10, "views": 6000},
    {"name": "Toy Story", "likes": 9, "views": 10000}]

# for i in range(len(data)):
#     response = requests.put(BASE + 'video/' + str(i), data[i])
#     print(response.json())

for i in range(len(data)):
    response = requests.patch(BASE + 'video/' + str(i), data[i])
    print(response.json())

# Request video_id input from user 
# video_id= int(input("Please enter video ID: ").strip())

response = requests.patch(BASE + '/video/2', {'name': 'Moby Dick'})

input()
response = requests.get(BASE + 'video/2')
print(response.json())