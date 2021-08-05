import json
import decimal

class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			if o % 1 > 0:
				return float(o)
			else:
				return int(o)
		return super(DecimalEncoder, self).default(o)

def generate_response(status, body, headers={}):
	print(f"Status Code: {status}, Body: {body}")
	return {
		"statusCode": status,
		"body": json.dumps(body, indent=4, cls=DecimalEncoder),
		"headers": headers
	}
