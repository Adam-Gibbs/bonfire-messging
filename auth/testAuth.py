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

	def endpoint_test(self, event, context):
		return self.generate_response(200, {"status": True})

	def endpoint_test_auth(self, event, context):
		return self.generate_response(200, {"Hello world": True})

	def generate_response(self ,status, body, headers={}):
		return {
			"statusCode": status,
			"body": json.dumps(body, indent=4, cls=DecimalEncoder),
			"headers": headers
		}
