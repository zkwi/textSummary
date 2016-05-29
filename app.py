import os
from flask import Flask, request
import json
from textsummary import TextSummary
app = Flask(__name__)

@app.route('/api/CalcSummary/', methods=['GET', 'POST'])
def CalcSummary():
	data = request.data
	data = data.decode(encoding="utf-8")
	content = json.loads(data)
	text = content['text']
	title = content['title']
	textsummary = TextSummary()
	textsummary.SetText(title, text)
	summary = textsummary.CalcSummary()
	print(summary)
	return json.dumps(summary)

@app.route('/')
def index():
	# 直接返回静态文件
	return app.send_static_file("index.html")
if __name__ == '__main__':
	# app.run(debug=True)
	port = int(os.environ.get("PORT", "5000"))
	app.run(host='0.0.0.0', port=port,debug=True)