import api.getSummary
text = open("api/data.txt", encoding="utf-8").read()
results = api.getSummary.getSummary(text)