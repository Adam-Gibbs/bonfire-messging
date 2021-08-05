import boto3

USER_POOL_ID = 'eu-west-2_xUNInjJwa'
CLIENT_ID = '8gjhsrum4alfi1u9i6prargi2'

def lambda_handler(event, context):
	print("start")
	for field in ["username", "email", "password"]:
		if not event.get(field):
			return {"success": False, 'message': f"{field} is not present", "data": None}

	username = event['username']
	email = event["email"]
	password = event['password']
	print(f"username: {username}, email: {email}, password: {password}")

	client = boto3.client('cognito-idp')
	try:
		print("try")
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

		print(resp)
	except client.exceptions.UsernameExistsException as e:
		return {
			"success": False,
			"message": "This username already exists",
			"data": None
		}

	except client.exceptions.InvalidPasswordException as e:
		return {
			"success": False,
			"message": "Password should have Caps,\
						Special chars, Numbers",
			"data": None
		}

	except client.exceptions.UserLambdaValidationException as e:
		return {
			"success": False,
			"message": "Email already exists",
			"data": None
		}

	except Exception as e:
		return {
			"success": False,
			"message": str(e),
			"data": None
		}

	return {
		"success": True,
		"message": "Please confirm your signup, \
					check Email for validation code",
	}
