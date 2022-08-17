import json
import requests
path = "https://gist.githubusercontent.com/champaksworldcreate/54a28ed28270fc924c5711edbb5649c7/raw/cdc21169a201a252cfa98a79a4ed4aba4c6aa7b1/listofquizzes.json"

# question = '{"questionno":1,"question":"What is the capital of Japan","option1":"Hukulganj","option2":"Peelikothi","option3":"Jaunpur","option4":"Tokyo","correct":"4"}'

response = requests.get(path)
print(response)
print(response.status_code)
print(type(response),response.text)
jsonoutput = json.loads(response.text)
print(jsonoutput, type(jsonoutput))
print(type(jsonoutput["quizzes"]),jsonoutput["quizzes"])

# import json
# {
#     "Data Structure ":[
#         {
#             "Name" : "Trees",
#             "Course" : "Introduction of Trees",
#             "Content" : ["Binary Tree", "BST","Generic Tree"]
#         },
#         {
#             "Name" : "Graphs",
#             "Topics" :["BFS", "DFS", "Topological Sort"]
#
#         }
#     ]
#
#
#
# }