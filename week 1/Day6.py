import json
data='{"name":"AI Bot","skills":["Python","MIL","NLP"]}'
print(data)
parsed=json.loads(data)
print(parsed["skills"][0])