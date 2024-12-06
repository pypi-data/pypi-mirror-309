import boto3
from botocore.exceptions import ClientError
import os
import secrets
import string

cognito_client = boto3.client("cognito-idp", os.environ["REGION"])

COGNITO_USER_POOL_ID = os.environ["BELINA_ADMIN_COGNITO_USER_POOL_ID"]
COGNITO_USER_CLIENT_ID = os.environ["BELINA_ADMIN_COGNITO_CLIENT_ID"]


def get_user_groups(username):
    client = boto3.client("cognito-idp")

    try:
        response = cognito_client.admin_list_groups_for_user(
            UserPoolId=COGNITO_USER_POOL_ID, Username=username
        )

        # Check if the user is in any groups
        if response["Groups"]:
            return [group["GroupName"] for group in response["Groups"]]
        else:
            return False

    except client.exceptions.UserNotFoundException:
        # Handle the case where the user is not found
        print(f"User {username} not found.")
        return False

    except Exception as e:
        # Handle other potential exceptions
        print(f"An error occurred: {str(e)}")
        return False


def checkIfGroupHasUsers(group_id):

    try:
        response = cognito_client.list_users_in_group(
            UserPoolId=COGNITO_USER_POOL_ID, GroupName=group_id, Limit=1
        )
        print("a", response)
        # If the response contains at least one user, the group has users
        return True if len(response["Users"]) > 0 else False

    except cognito_client.exceptions.ResourceNotFoundException:
        # If the group is not found, it has no users
        return False

    except Exception as e:
        # Handle other exceptions
        print(f"Error checking group users: {e}")
        return False


def process_data(data):
    result = []
    for item in data:
        has_users = checkIfGroupHasUsers(item["group_id"])
        result.append(
            {
                "group_description": item["group_description"],
                "data_id": item["data_id"],
                "group_id": item["group_id"],
                "group_name": item["group_name"],
                "is_assigned": has_users,
            }
        )
    return result


def reset_password(user_params, permanent, user_pool_id=None):
    """
    The `cognito_reset_password` function resets the password for a user in a Cognito user pool using
    the AWS SDK for Python (Boto3).

    :param user_params: The `user_params` parameter is a dictionary that contains the following
    information:
    :return: a dictionary with the following keys:
    """
    try:
        client = boto3.client("cognito-idp")

        params = {
            "Password": user_params["password"],
            "UserPoolId": user_pool_id if user_pool_id else COGNITO_USER_POOL_ID,
            "Username": user_params["username"],
            "Permanent": True if permanent else False,
        }

        response = client.admin_set_user_password(**params)
        print("**********", response)
        if response:
            return True
        else:
            return False

    except Exception:
        return False


def admin_global_sign_out(username):
    """
    Perform a global sign-out for a specific user by username.

    :param username: The username of the user to perform the global sign-out for.
    :return: A dictionary containing the response from the global sign-out operation.
    """
    try:
        # Call the admin global sign-out API
        cognito_client.admin_user_global_sign_out(
            UserPoolId=COGNITO_USER_POOL_ID, Username=username
        )
        return True
    except Exception as e:
        print("Error performing admin global sign-out:", e)
        return False


def authenticate_user(username, password):
    try:
        # Attempt to authenticate the user
        response = cognito_client.admin_initiate_auth(
            UserPoolId=COGNITO_USER_POOL_ID,
            ClientId=COGNITO_USER_CLIENT_ID,
            AuthFlow="ADMIN_USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": password},
        )
        print("hey", response)
        # If authentication succeeds, the password is correct
        return True
    except ClientError as e:
        # If authentication fails, check the error code
        error_code = e.response["Error"]["Code"]
        if error_code == "NotAuthorizedException":
            # Password is incorrect
            return False
        else:
            # Other errors
            raise e  # Raise the exception for other errors


def create_cognito_group(group_name, user_pool_id):
    try:
        # Create the group
        response = cognito_client.create_group(
            GroupName=group_name, UserPoolId=user_pool_id
        )
        # Check for successful creation
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print(f"Group '{group_name}' created successfully.")
            return True
        else:
            print(f"Failed to create group '{group_name}'.")
            return False

    except Exception as e:
        print(f"Error creating group: {e}")
        return False


def generate_password():
    while True:
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        punctuation = string.punctuation.replace(" ", "")  # Exclude spaces

        # Combine character sets based on policy requirements
        characters = lowercase + uppercase + digits + punctuation
        password = "".join(secrets.choice(characters) for _ in range(8))

        # Validate password based on policy
        if (
            any(char.islower() for char in password)
            and any(char.isupper() for char in password)
            and any(char.isdigit() for char in password)
            and any(char in punctuation for char in password)
        ):
            return password


def activate_deactivate_user(username, activate):
    try:
        print("activate", activate)
        params = {
            "UserPoolId": COGNITO_USER_POOL_ID,
            "Username": username,
        }
        if activate:
            cognito_client.admin_enable_user(
                UserPoolId=params["UserPoolId"], Username=username
            )
        else:
            cognito_client.admin_disable_user(
                UserPoolId=params["UserPoolId"], Username=username
            )
        return {"success_status": True}
    except Exception as error:
        return {"success_status": False, "message": str(error)}


def cognito_check_user_exists(username):
    try:
        response = cognito_client.admin_get_user(
            UserPoolId=COGNITO_USER_POOL_ID, Username=username
        )
        return response  # User exists
    except cognito_client.exceptions.UserNotFoundException:
        return False  # User does not exist


def update_user_custom_attributes(username, custom_attributes):
    try:
        params = {
            "UserPoolId": COGNITO_USER_POOL_ID,
            "Username": username,
            "UserAttributes": [
                {"Name": attr["name"], "Value": attr["value"]}
                for attr in custom_attributes
            ],
        }
        cognito_client.admin_update_user_attributes(**params)
        return {"success_status": True}
    except Exception as error:
        return {"success_status": False, "message": str(error)}


def cognito_user(username):
    """
    The function `cognito_user` retrieves user attributes from a Cognito user pool using the provided
    username.

    :param username: The `username` parameter is the username of the Cognito user for which you want to
    retrieve the user attributes
    :return: The function `cognito_user` returns the user attributes of a Cognito user with the given
    username. If the user is found, it returns the user attributes as a list. If there is an error, it
    returns a dictionary with the keys 'success_status' and 'message'.
    """
    params = {
        "UserPoolId": COGNITO_USER_POOL_ID,
        "Username": username,
    }
    try:
        result = cognito_client.admin_get_user(**params)
        return {"success_status": True, "data": result["UserAttributes"]}
    except Exception as error:
        print("Error:", error)

        return {"success_status": False, "message": str(error)}


def cognito_reset_password(user_params):
    """
    The `cognito_reset_password` function resets the password for a user in a Cognito user pool using
    the AWS SDK for Python (Boto3).

    :param user_params: The `user_params` parameter is a dictionary that contains the following
    information:
    :return: a dictionary with the following keys:
    """
    try:
        client = boto3.client("cognito-idp")

        params = {
            "Password": user_params["password"],
            "UserPoolId": COGNITO_USER_POOL_ID,
            "Username": user_params["username"],
            "Permanent": True,
        }

        response = client.admin_set_user_password(**params)

        if response:
            print("success")
            return {
                "success_status": True,
                "data": response,
            }

        return {
            "success_status": False,
        }

    except Exception:
        return {
            "success_status": False,
        }
