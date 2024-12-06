import string
import secrets
import json
from datetime import datetime
import uuid
import boto3
import jwt
import os
import random
import re
from psycopg2 import sql

from cryptography.fernet import Fernet

dynamodb = boto3.resource("dynamodb")
ses_client = boto3.client("ses", region_name=os.environ["REGION"])

def generate_session_token(dict_key,payload, expiration_time,jwt_secret):
    """
    The function `generate_session_token` generates a session token for a given user name using a JWT
    secret key and an expiration time of 10 minutes.

    :param user_name: The `user_name` parameter is the name of the user for whom the session token is
    being generated
    :return: a session token, which is a JSON Web Token (JWT) encoded with the user's name and
    expiration time.
    """
    token = jwt.encode(
        {
            dict_key: payload,
            "exp": int(expiration_time.timestamp()),
        },
        jwt_secret,
        algorithm="HS256",
    )
    return token

def generate_otp():
    otp = random.randint(100000, 999999)  # Generates a 6-digit number
    return otp

def remove_duplicates(items, key):
    unique_items = []
    seen_keys = set()
    for item in items:
        key_value = item[key]
        if key_value not in seen_keys:
            unique_items.append(item)
            seen_keys.add(key_value)
    return unique_items


def batch_get_country_names(holidays_data, table_name, data_id):
    table = dynamodb.Table(table_name)

    # Prepare the list of keys for batch get
    keys = [
        {"data_id": data_id, "country_id": item["country_id"]} for item in holidays_data
    ]
    unique_items = remove_duplicates(keys, "country_id")
    # Batch get items
    response = table.meta.client.batch_get_item(
        RequestItems={
            table_name: {
                "Keys": unique_items,
                "ProjectionExpression": "country_id, country_name",
            }
        }
    )
    # Create a dictionary mapping country_id to country_name
    country_map = {
        item["country_id"]: item.get("country_name")
        for item in response["Responses"][table_name]
    }
    # Add country_name to each holiday item
    for item in holidays_data:
        item["country_name"] = country_map.get(item["country_id"], "Unknown")
    return holidays_data


def query_recursive(table, limit, **kwargs):
    """
    Recursively query the table until we have enough items or there are no more to fetch.
    """
    items = []
    last_evaluated_key = None
    total_scanned = 0
    while len(items) < limit:
        new_limit = limit - len(items)
        print(new_limit, "new_limit")
        kwargs["Limit"] = new_limit
        if "FilterExpression" in kwargs:
            kwargs.pop("Limit")
        if last_evaluated_key:
            kwargs["ExclusiveStartKey"] = last_evaluated_key

        response = table.query(**kwargs)

        items.extend(response.get("Items", []))
        last_evaluated_key = response.get("LastEvaluatedKey")
        total_scanned += response.get("ScannedCount", 0)

        if not last_evaluated_key:
            break

    if last_evaluated_key:
        kwargs["Limit"] = 1
        if "FilterExpression" not in kwargs:
            kwargs["ExclusiveStartKey"] = last_evaluated_key
            print(kwargs, "ssssssssssssssssss")
            last_response = table.query(**kwargs)
            print("last_response", last_response)
            if last_response["Count"] < 1:
                print("coming")
                last_evaluated_key = None

    return items, total_scanned, last_evaluated_key


def dynamodb_query_recursive(table, limit, **kwargs):
    """
    Recursively query the table until we have enough items or there are no more to fetch.
    """
    items = []
    last_evaluated_key = None
    total_scanned = 0
    while len(items) < limit:
        new_limit = limit - len(items)
        kwargs["Limit"] = new_limit
        if last_evaluated_key:
            kwargs["ExclusiveStartKey"] = last_evaluated_key

        response = table.query(**kwargs)

        items.extend(response.get("Items", []))
        last_evaluated_key = response.get("LastEvaluatedKey")
        total_scanned += response.get("ScannedCount", 0)

        if not last_evaluated_key:
            break
    if last_evaluated_key:
        kwargs["Limit"] = 1
        kwargs["ExclusiveStartKey"] = last_evaluated_key
        print(kwargs, "ssssssssssssssssss")
        last_response = table.query(**kwargs)
        print("last_response", last_response)
        if last_response["Count"] < 1 or not last_response.get("LastEvaluatedKey"):
            print("coming")
            last_evaluated_key = None

    return items, total_scanned, last_evaluated_key


def generate_update_expression(data):
    update_expression = "SET "
    expression_attribute_values = {}
    for key, value in data.items():
        update_expression += f"{key} = :{key}, "
        expression_attribute_values[f":{key}"] = value
    update_expression = update_expression.rstrip(
        ", "
    )  # Remove the trailing comma and space
    return update_expression, expression_attribute_values


def is_valid_uuid(id):
    try:
        # Attempt to create a UUID object
        uuid_obj = uuid.UUID(id, version=4)
        return str(uuid_obj)
    except ValueError:
        print(ValueError)
        return False


def format_search_data(search_data):
    parts = []
    for key, value in search_data.items():
        parts.extend([value.upper(), value.lower()])
    return "~".join(parts)


def format_list_query(
    query, table_name, search_fields=None, filter_fields=None, projection_fields=None
):
    order_by_clause = "created_at DESC"
    where_conditions = []
    query_params = []

    query_sql = None

    if query:
        if "sort" in query:
            field, order = query["sort"].split("+")
            sort_order = "ASC" if order == "asc" else "DESC"
            order_by_clause = "{} {}".format(field, sort_order)

        if "search" in query:
            trimmed_value = query["search"].strip()
            print("err", len(trimmed_value))
            if len(trimmed_value) > 0:
                search = query["search"]
                # escaped_search = search.replace("'", "''")
                search_conditions = [
                    sql.SQL("{} ILIKE %s").format(sql.Identifier(field))
                    for field in search_fields
                ]
                where_conditions.append(
                    sql.SQL("({})").format(sql.SQL(" OR ").join(search_conditions))
                )
                for field in search_fields:
                    query_params.append("%" + search + "%")
            else:
                where_conditions.append(sql.SQL("1=0"))
        if filter_fields:
            filter_conditions = [
                sql.SQL("{} IN %s").format(sql.Identifier(field))
                for field in filter_fields
                if query.get(field)
            ]
            if filter_conditions:
                where_conditions.append(
                    sql.SQL("({})").format(sql.SQL(" AND ").join(filter_conditions))
                )
                query_params += [
                    tuple(query[field].split(","))
                    for field in filter_fields
                    if query.get(field)
                ]
    # query_sql = sql.SQL("""
    #     SELECT * FROM banks WHERE {} ORDER BY {};""").format(sql.SQL(' AND ').join(where_conditions), sql.SQL(order_by_clause))
    print("where_conditions", where_conditions)

    # query_sql = sql.SQL("""
    #     SELECT {projection} FROM {table_name}{where_clause} ORDER BY {order_by_clause};
    # """).format(
    #     projection=sql.SQL(', ').join(map(sql.Identifier, projection_fields)),
    #     table_name=sql.Identifier(table_name),
    #     where_clause=sql.SQL(' WHERE {}').format(sql.SQL(' AND ').join(where_conditions)) if where_conditions else sql.SQL(''),
    #     order_by_clause=sql.SQL(order_by_clause)
    # )
    query_sql = sql.SQL(
        """
        SELECT {projection} FROM {table_name}{where_clause}{order_by_clause};
    """
    ).format(
        projection=sql.SQL(", ").join(map(sql.Identifier, projection_fields)),
        table_name=sql.Identifier(table_name),
        where_clause=(
            sql.SQL(" WHERE {}").format(sql.SQL(" AND ").join(where_conditions))
            if where_conditions
            else sql.SQL("")
        ),
        order_by_clause=sql.SQL(" ORDER BY {}").format(sql.SQL(order_by_clause)),
    )
    return query_sql, query_params


def is_invalid_password(password, confirm_password, current_password=None,password_type=None):
    """
    The function `is_invalid_password` checks if a password is valid based on certain criteria such as
    length, matching confirmation password, presence of uppercase, lowercase, digit, and allowed special
    characters, and absence of invalid characters
    :param password: The `password` parameter is the new password that the user wants to set
    :param confirm_password: The `confirm_password` parameter is used to confirm that the `password`
    parameter is entered correctly. It is used to check if the `password` and `confirm_password` values
    match
    :return: a string message if the password is invalid, and it is returning False if the password is
    valid.
    """
    # Check length
    if len(password) < 8 or len(confirm_password) < 8:
        return "New password and Confirm password must be at least 8 characters long."

    if current_password:
        if current_password == password:
            return f"{'Temporary' if password_type == 'reset' else 'Current'} and new passwords must differ"

    if password != confirm_password:
        return "Passwords do not match."
    allowed_symbols = "!@#$%^&*:./?=+-_[]{}()<>"

    # Check for at least one uppercase letter, one lowercase letter, one digit, and one of the allowed special characters
    if not (
        re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"\d", password)
        and re.search(f"[{re.escape(allowed_symbols)}]", password)
    ):
        return "New password must contain at least one allowed symbol, one lowercase, one uppercase, and one digit character."

    # Define allowed characters
    allowed_characters = set(string.ascii_letters + string.digits + allowed_symbols)

    # Check for any characters other than allowed characters
    if set(password) - allowed_characters:
        return "New password contains invalid characters."

    return False


def send_ses_email_with_template(
    destination_id, source_id, template_name, template_data
):
    print("template_name", template_name)
    params = {
        "Destination": {
            "ToAddresses": [destination_id],
        },
        "Source": source_id,
        "Template": template_name,
        "TemplateData": json.dumps(template_data),
    }
    print("hello", params)
    print("tenplate", params["Template"])
    try:
        response = ses_client.send_templated_email(**params)
        print("Email sent successfully:", response)
        if response and response.get("MessageId"):
            return True
        return False
    except Exception as e:
        print("Error sending email:", e)
        return False


def convert_to_json_serializable(data):
    # This function recursively converts ObjectId objects to their string representation
    # if isinstance(data, datetime):
    #     return str(data)
    # if isinstance(data, ObjectId):
    #     return str(data)
    if isinstance(data, list):
        return [convert_to_json_serializable(item) for item in data]
    if isinstance(data, dict):
        return {key: convert_to_json_serializable(value) for key, value in data.items()}
    return data


def response_handler(status_code, message, errors=None):
    response_body = {"message": message}
    if errors:
        response_body["errors"] = errors
    return {
        "statusCode": status_code,
        "headers": headers,
        "body": json.dumps(response_body),
    }


def epoch_timestamp():
    epoch_seconds = int(datetime.now().timestamp())
    return epoch_seconds


# This is defining a dictionary called `headers` that contains \various HTTP headers that can be used
# in a response to a client. These headers include the `Content-Type` header, which specifies the
# format of the response (in this case, JSON), and several `Access-Control-Allow-*` headers, which are
# used to control access to the resource from different domains. The `*` values for the
# `Access-Control-Allow-Headers` and `Access-Control-Allow-Methods` headers indicate that any header
# or method is allowed.
headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": True,
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Methods": "*",
}


def generate_secure_password(length=12, use_special_characters=True):
    """
    Generates a secure password with the given length.

    :param length: Length of the password (default is 12)
    :param use_special_characters: Boolean to include special characters (default is True)
    :return: A securely generated password as a string
    """

    # Base alphabet: letters and digits
    alphabet = string.ascii_letters + string.digits

    # Add special characters if required (excluding space)
    if use_special_characters:
        special_characters = "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"
        alphabet += special_characters

    # Ensure password contains at least one character of each type
    password = [
        secrets.choice(string.ascii_lowercase),  # At least one lowercase
        secrets.choice(string.digits),  # At least one digit
    ]

    if use_special_characters:
        password.append(
            secrets.choice(special_characters)
        )  # At least one special character

    password = [char for char in password if char != ' ']

    # Fill the rest of the password length with random choices from the alphabet
    while len(password) < length - 1:
        char = secrets.choice(alphabet)
        if char != ' ':  # Skip spaces if accidentally included
            password.append(char)

    # Shuffle to ensure the order is random
    secrets.SystemRandom().shuffle(password)
    password.insert(0, secrets.choice(string.ascii_uppercase))  # Insert at least one uppercase at the start (index 0)

    # Convert list to string and return
    return "".join(password)



def send_email(
    recepient_email, from_email, template_arn, template_data, region="us-east-1"
):
    print("receip", recepient_email, from_email)
    """
    The function `send_email` sends an email using the Amazon Pinpoint Email service in the specified
    region, using a template and template data.
    :param recepient_email: The email address of the recipient to whom the email will be sent
    :param from_email: The email address from which the email will be sent
    :param template_arn: The `template_arn` parameter is the Amazon Resource Name (ARN) of the email
    template that you want to use for sending the email. The ARN uniquely identifies the template in
    Amazon Pinpoint
    :param template_data: The `template_data` parameter is a dictionary that contains the data to be
    used in the email template. This data will be used to populate the placeholders in the email
    template. The keys in the dictionary should match the placeholders in the template. For example, if
    the template has a placeholder `{name}`,
    :param region: The region where the Amazon Pinpoint service is located. The default value is
    'us-east-1', which is the US East (N. Virginia) region, defaults to us-east-1 (optional)
    :return: the response from the `client.send_email()` method if the email is sent successfully. If
    there is an error while sending the email, it returns a dictionary with a status code of 500 and a
    message indicating the error.
    """
    client = boto3.client("pinpoint-email", region_name=region)
    try:
        print("send email comman helper")
        response = client.send_email(
            FromEmailAddress=from_email,
            Destination={"ToAddresses": [recepient_email]},
            Content={
                "Template": {
                    "TemplateArn": template_arn,
                    "TemplateData": json.dumps(template_data),
                }
            },
        )
        print("response", response)
        print(f"Email response for {recepient_email}: {response}")
        return response
    except Exception as e:
        print(f"Error sending email to {recepient_email}: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"messages": "Error while sending email"}),
        }


def send_pinpoint_email(destination_id, source_id, template_data, template_arn):
    """
    The function `send_pinpoint_email` sends an email using the Amazon Pinpoint Email service in Python.
    :param destination_id: The `destination_id` parameter is the email address of the recipient who will
    receive the email
    :param source_id: The source_id parameter is the email address from which the email will be sent
    :param template_data: The `template_data` parameter is a dictionary that contains the data to be
    used in the email template. It should be in the format of key-value pairs, where the keys correspond
    to the placeholders in the email template and the values are the actual values to be substituted in
    the template
    :param template_arn: The `template_arn` parameter is the Amazon Resource Name (ARN) of the email
    template that you want to use for sending the email. The ARN uniquely identifies the template in
    Amazon Pinpoint
    :return: a boolean value indicating whether the email was sent successfully or not. It returns True
    if the email was sent successfully and False if there was an error or if the response status code is
    not 200.
    """
    pinpoint = boto3.client("pinpoint-email", region_name=os.environ["REGION"])
    params = {
        "Destination": {
            "ToAddresses": [destination_id],
        },
        "Content": {
            "Template": {
                "TemplateArn": template_arn,
                "TemplateData": template_data,
            },
        },
        "FromEmailAddress": source_id,
    }

    try:
        response = pinpoint.send_email(**params)
        print("Email sent successfully:", response)
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") != 200:
            return False
        return True
    except Exception as error:
        print("Failed to send email:", error)
        return False


def encode_password(password):
    """
    The function `encode_password` takes a password as input and  \
        encrypts it using the Fernet encryption
    algorithm.

    :param password: The `password` parameter is the string  \
    that you want to encrypt
    :return: the encrypted version of the password.
    """
    f = Fernet(b"ti6fqefxBIm-d9nqvJM0lTZcXqnlTW8M2r25ftBHWcM=")
    encrypted_data = f.encrypt(password)
    return encrypted_data


def decrypt_password(password):
    """
    The function `decrypt_password` takes an encrypted password as input, \
    decrypts it using a Fernet
    key, and returns the decrypted password as a string.

    :param password: The `password` parameter is the encrypted password \
    that needs to be decrypted
    :return: The decrypted password data as a string.
    """
    f = Fernet(b"ti6fqefxBIm-d9nqvJM0lTZcXqnlTW8M2r25ftBHWcM=")
    decrypted_data = f.decrypt(password)
    return decrypted_data.decode()
