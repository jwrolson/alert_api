import json
import jsonschema
from jsonschema import validate
from flask as f
import bigpanda

app = f.Flask(__name__)

def validate_alert(data):
	alert_schema = {
	    "type" : "object",
	    "properties" : {
	        "source" : {"type" : "string"},
	        "name" : {"type" : "string"},
	        "status" : {"type" : "string"},
    		},
	}
	try:
		alert = json.loads(data)
		validate(alert, alert_schema)
		alert_valid = True
    	except jsonschema.exceptions.ValidationError as ve:
    		alert_valid = False
	return alert_valid

def send_alert(alert):
	bp = bigpanda.Client(api_token='')
	bp_alert = bp.alert(**alert)
	bp_alert.send()

def transform_alert(data):
	data = json.loads(data)
	alert = {}
	alert['status'] = data.get('')
	alert['subject'] = data.get('')
	alert['check'] = data.get('')
	alert['description'] = data.get('')
	alert['cluster'] = data.get('')
	alert['timestamp'] = data.get('')
	alert['primary_attr'] = data.get('', default='host')
	alert['secondary_attr'] = data.get('', default='check')
	return alert

@app.route("/alert", methods=['POST'])
def splunk_webhook():
	json_request = f.request.json
	if validate_alert(json_request):
		alert = transform_alert(json_request)
		send_alert(alert)
	return "Alert sent."

@app.route('/healthcheck')
def hello_world():
	return 'Alive.'

if __name__ == '__main__':
	app.run(host='0.0.0.0', threaded=True)
