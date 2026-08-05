from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
	return "DNS Logger running"

if __name__ == '__main__':
	app.run(debug=True, port=1515)



