import boto3
import os
from botocore.exceptions import ClientError

client = boto3.client('cognito-idp', region_name='eu-west-1')


def generate_token(user_type):
    try:
        if user_type == "admin":
            # user_pool_id = os.environ.get('BELINA_ADMIN_COGNITO_USER_POOL_ID')
            # client_id = os.environ.get('BELINA_ADMIN_COGNITO_CLIENT_ID')
            # username = os.environ.get('USERNAME')
            # password = os.environ.get('PASSWORD')
            user_pool_id = "eu-west-1_4c8uNLjlV"
            client_id = "4qakh85fgoojfhog0eqo2mcvo1"
            username = "akhilesh.b+apitest@7edge.com"
            password = "Admin@123"
        if user_type == "organisation_user":
            # user_pool_id = os.environ.get('BELINA_ADMIN_COGNITO_USER_POOL_ID')
            # client_id = os.environ.get('BELINA_ADMIN_COGNITO_CLIENT_ID')
            # username = os.environ.get('USERNAME')
            # password = os.environ.get('PASSWORD')
            user_pool_id = "eu-west-1_nzkKCHvms"
            client_id = "5jnt6pqn93liml25lvhvqj8f9t"
            username = "kmbol#akhilesh.b@7edge.com"
            password = "Admin@123"
        if user_pool_id is None or client_id is None or username is None or password is None:
            print("Required environment variables are not set.")
            return

        response = client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        token = response['AuthenticationResult']['IdToken']
        os.environ['TOKEN'] = token
        print(f'export {user_type}="{token}"')
    except ClientError as e:
        print(e)
        os.environ['TOKEN'] = user_type



generate_token('admin')
generate_token('organisation_user')