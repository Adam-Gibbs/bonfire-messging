import boto3
import json
from endpoints.helpers.returns import generate_response

USER_POOL_ID = 'eu-west-2_xUNInjJwa'
CLIENT_ID = '8gjhsrum4alfi1u9i6prargi2'

def lambda_handler(event, context):
	params = json.loads(event.get("body"))
	for field in ["username", "email", "password"]:
		if not params.get(field):
			return generate_response(400,
				{
					"success": False,
					'message': f"{field} is not present", 
					"data": None
				}
			)

	username = params['username']
	email = params["email"]
	password = params['password']

	client = boto3.client('cognito-idp')
	try:
		resp = client.sign_up(
			ClientId=CLIENT_ID,
			Username=username,
			Password=password,
			UserAttributes=[
				{
					'Name': "email",
					'Value': email
				}
			],
			ValidationData=[
				{
					'Name': "email",
					'Value': email
				},
				{
					'Name': "custom:username",
					'Value': username
				}
			]
		)

	except client.exceptions.UsernameExistsException as e:
		return generate_response(400, 
			{
				"success": False,
				"message": "This username already exists",
				"data": None
			}
		)

	except client.exceptions.InvalidPasswordException as e:
		return generate_response(400,
			{
				"success": False,
				"message": "Password should have Caps,\
							Special chars, Numbers",
				"data": None
			}
		)

	except client.exceptions.UserLambdaValidationException as e:
		return generate_response(400, 
			{
				"success": False,
				"message": "Email already exists",
				"data": None
			}
		)

	except Exception as e:
		return generate_response(400,
			{
				"success": False,
				"message": str(e),
				"data": None
			}
		)

	return generate_response(200,
		{
			"success": True,
			"message": "Please confirm your signup, \
						check Email for validation code",
		}
	)
