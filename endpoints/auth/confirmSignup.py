import json
import boto3
from helpers.returns import generate_response

USER_POOL_ID = 'eu-west-2_xUNInjJwa'
CLIENT_ID = '8gjhsrum4alfi1u9i6prargi2'

def lambda_handler(event, context):
    params = json.loads(event.get("body"))
    client = boto3.client('cognito-idp')
    
    try:
        username = params['username']
        code = params['code']
        
        response = client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            ConfirmationCode=code,
            ForceAliasCreation=False,
        )

        print(response)

    except client.exceptions.UserNotFoundException:
        generate_response(400, {"success": False, "message": "Username doesn't exists"})
        # return event
        
    except client.exceptions.CodeMismatchException:
        generate_response(400, {"success": False, "message": "Invalid Verification code"})
        
    except client.exceptions.NotAuthorizedException:
        generate_response(400, {"success": False, "message": "User is already confirmed"})
    
    except Exception as e:
        generate_response(400, {"success": False, "message": f"Unknown error {e.__str__()} "})
      
    generate_response(200, event)
