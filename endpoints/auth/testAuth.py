from endpoints.helpers.returns import generate_response;

def endpoint_test_auth(event, context):
	return generate_response(200, {"Hello world": True})