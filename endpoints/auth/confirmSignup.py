import json
import boto3

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
        return {"success": False, "message": "Username doesn't exists"}
        # return event
        
    except client.exceptions.CodeMismatchException:
        return {"success": False, "message": "Invalid Verification code"}
        
    except client.exceptions.NotAuthorizedException:
        return {"success": False, "message": "User is already confirmed"}
    
    except Exception as e:
        return {"success": False, "message": f"Unknown error {e.__str__()} "}
      
    return event
