import decimal
import json
import re
import os
import jwt
from datetime import datetime, timedelta
from marshmallow import Schema, fields, validate, ValidationError
from jwt.exceptions import ExpiredSignatureError, DecodeError
from lib.helper import headers
from boto3.dynamodb.conditions import Key, Attr


class Encoder(json.JSONEncoder):
    """
    Encoder Function for all returns
    Accessibility (private)
    @returns (Dictionary)
    """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, bytes):
            return o.decode("utf-8")
        if isinstance(o, datetime):
            return o.isoformat()
        if hasattr(o, "__dict__"):
            return o.__dict__
        return json.JSONEncoder.default(self, o)


# class jsonEncoder(json.JSONEncoder):
#     """
#     /**
#       * * Encoder Function for all returns
#       * ? Accessibilty (private)
#       * @returns (Dictionary)
#     */
#     """

#     def default(self, o):
#         if isinstance(o, decimal.Decimal):
#             return str(o)
#         if isinstance(o, bytes):
#             return str(o)
#         if isinstance(o, ObjectId):  # Handle ObjectId objects
#             return str(o)
#         if isinstance(o, datetime):
#             return o.isoformat()
#         if isinstance(o, object):
#             return o.__dict__
#         return o.__dict__


def epoch_timestamp():
    epoch_seconds = int(datetime.now().timestamp())
    return epoch_seconds


class CurrencyTypeSchema(Schema):
    """
    The function defines fields for currency name, code, and symbol with validation rules and a data
    loading method that normalizes string values.

    :param data: The code snippet you provided defines a schema for handling currency data. The `load`
    method is used to preprocess the data before loading it into the schema
    :return: The `load` method is returning the processed `data` dictionary after stripping
    leading/trailing spaces and normalizing internal spaces in string values.
    """

    currency_name = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=1,
                max=50,
                error="Currency name must be between 1 and 50 characters.",
            ),
        ],
        error_messages={"required": "Currency name cannot be empty"},
    )
    currency_code = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=1, max=4, error="Currency Code must be between 1 and 4 characters."
            ),
        ],
        error_messages={"required": "Currency Code cannot be empty"},
    )
    symbol = fields.String(
        required=True,
        validate=[
            validate.Length(
                min=1, max=3, error="Symbol must be between 1 to 3 characters, "
            ),
        ],
    )

    def load(self, data, *args, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                # Strip leading/trailing spaces and normalize internal spaces
                data[key] = re.sub(r"\s+", " ", value.strip())
        return super().load(data, *args, **kwargs)


def non_empty_string(value):
    if not value.strip():
        raise ValidationError("menu items cannot be an empty string.")


class PrivilegesValidator:
    def __call__(self, privileges):
        if "*" in privileges and len(privileges) > 1:
            raise ValidationError(
                "If '*' is present, no other privileges can be specified."
            )
        for privilege in privileges:
            if privilege not in [
                "*",
                "organisations",
                "banks",
                "holidays",
                "currency_types",
                "tax_methods",
                "tax_parameters",
                "countries",
            ]:
                raise ValidationError(f"Invalid privilege: {privilege}")


class UserGroupSchema(Schema):
    # The `UserGroupSchema` class defines a schema for user groups with validation rules for user group
    # name, description, and privileges.
    user_group_name = fields.String(
        required=True,
        validate=validate.Length(min=1, error="User group name cannot be empty."),
        error_messages={"required": "User group name is required field"},
    )
    user_group_description = fields.String(
        required=True,
        validate=validate.Length(min=1, error="User group description cannot be empty"),
        error_messages={"required": "User group description is required field"},
    )
    privileges = fields.List(
        fields.String(validate=non_empty_string),
        required=True,
        validate=[
            validate.Length(min=1, error="Privileges cannot be empty."),
            PrivilegesValidator(),
        ],
        error_messages={"required": "Privileges is a required field"},
    )

    def load(self, data, *args, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return super().load(data, *args, **kwargs)


def generate_session_token(user_name, object_id):
    """
    The function `generate_session_token` generates a session token for a given user name using a JWT
    secret key and an expiration time of 10 minutes.

    :param user_name: The `user_name` parameter is the name of the user for whom the session token is
    being generated
    :return: a session token, which is a JSON Web Token (JWT) encoded with the user's name and
    expiration time.
    """
    jwt_secret = os.environ["JWT_SECRET_KEY"]
    expiration_time = datetime.now() + timedelta(minutes=30)
    token = jwt.encode(
        {
            "username": user_name,
            "object_id": object_id,
            "exp": int(expiration_time.timestamp()),
        },
        jwt_secret,
        algorithm="HS256",
    )
    return token


def is_token_expired(token, jwt_secret):
    """
    The function `is_token_expired` checks if a given token has expired by decoding it using a JWT
    secret and handling different verification errors.
    :param token: The `token` parameter is the JWT (JSON Web Token) that needs to be checked for
    expiration. It is a string representation of the token
    :param jwt_secret: The `jwt_secret` parameter is a secret key used to sign and verify the JSON Web
    Token (JWT). It is a string value that should be kept secure and known only to the server that
    generates and verifies the tokens
    :return: The function is_token_expired returns either "expired" if the token has expired, "invalid"
    if there are verification errors, or a dictionary with the keys "success_status" and "data" if the
    token is successfully verified.
    """
    try:
        verified_token = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        return {"success_status": True, "data": verified_token}
    except ExpiredSignatureError:
        # Token has expired
        return "expired"
    except DecodeError:
        # Other verification errors
        return "invalid"  # Consider it expired for handling verification errors


# Define a schema for validating tax method data


class TaxMethodSchema(Schema):
    """
    Schema for validating tax method data.

    Attributes:
        tax_method (str): The tax method name.
        country (str): The country for which the tax method applies.
        is_default (bool): Indicates if the tax method is default.
        is_equivalent_to_paye (bool): Indicates if the tax method is equivalent to PAYE.
    """

    tax_method = fields.String(
        required=True,
        validate=validate.Length(min=1, max=25, error="Tax method cannot be empty."),
        error_messages={"required": "Tax method is required field"},
    )
    country = fields.String(
        required=True,
        validate=validate.Length(min=1, error="Country cannot be empty."),
        error_messages={"required": "Country is required field"},
    )
    is_default = fields.Boolean(
        required=True,
        validate=validate.OneOf([True, False], error="is_default must be a boolean."),
        error_messages={"required": "is_default is required field"},
    )
    is_equivalent_to_paye = fields.Boolean(
        required=True,
        validate=validate.OneOf(
            [True, False], error="is_equivalent_to_paye must be a boolean."
        ),
        error_messages={"required": "is_equivalent_to_paye is required field"},
    )
    # Custom data loader to strip whitespace from string fields

    def load(self, data, *args, **kwargs):
        """
        The loaded data with whitespace stripped from string fields.
        """
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return super().load(data, *args, **kwargs)


def get_organisation_details(
    organisation_id, get_type, table, countries_table, payment_table=None
):
    """
    Retrieves organization details based on the ID and optional type parameter.
    """
    try:
        projection_expression = "tenant_id, organisation_name, number_of_employees, registered_at, organisation_email_address, \
            organisation_phone_number_code,organisation_phone_number,organisation_status,country_id, country_name, organisation_id,domain_url,website_url, \
                  address_line1, address_line2, city, state_name,postal_code, rejected_reason"

        if get_type and get_type == "subdomain":
            projection_expression = (
                "organisation_id, organisation_status, domain_url, rejected_reason"
            )
            org_table_response = table.get_item(
                Key={"data_id": "BelinaPayroll", "organisation_id": organisation_id},
                ProjectionExpression=projection_expression,
            )
            if "Item" not in org_table_response:
                return {
                    "statusCode": 404,
                    "headers": headers,
                    "body": json.dumps(
                        {"success_status": False, "message": "Organisation not found"}
                    ),
                }
            org_item = org_table_response["Item"]
            organisation_status = org_item["organisation_status"]

            print("organisation_id", organisation_id)
            response = payment_table.query(
                KeyConditionExpression=Key("organisation_id").eq(organisation_id),
                ProjectionExpression=projection_expression,
                FilterExpression=Attr("payment_status").eq("succeeded"),
            )
            print("response", response)

            if not response.get("Items"):
                return {
                    "statusCode": 200,
                    "headers": headers,
                    "body": json.dumps(
                        {
                            "success_status": True,
                            "organisation_id": organisation_id,
                            "payment_status": "pending",
                            "organisation_status": 'pending',

                        }
                    ),
                }
            response_data = {
                "success_status": True,
                "organisation_id": organisation_id,
                "organisation_status": organisation_status,
                "payment_status": "succeded",
            }
            if organisation_status == "active":
                response_data["domain_url"] = (
                    f"{org_item['domain_url']}.{os.environ.get('DOMAIN_NAME')}",
                )
            elif organisation_status == "creating":
                response_data["organisation_status"] = "pending"
            elif organisation_status == "rejected":
                if not org_item["rejected_reason"] or org_item["rejected_reason"] == "":
                    response_data["is_generic"] = True
                    response_data["rejected_reason"] = ""
                else:
                    response_data["is_generic"] = False
                    response_data["rejected_reason"] = org_item["rejected_reason"]
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps(response_data),
            }

        response = table.get_item(
            Key={"data_id": "BelinaPayroll", "organisation_id": organisation_id},
            ProjectionExpression=projection_expression,
        )

        if "Item" not in response:
            return {
                "statusCode": 404,
                "headers": headers,
                "body": json.dumps(
                    {"success_status": False, "message": "Organisation not found"}
                ),
            }
        item = response['Item']
        if item['organisation_status'] == "rejected":
            if 'rejected_reason' not in item or not item["rejected_reason"] or item["rejected_reason"] == "":
                item["is_generic"] = True
            else:
                item["is_generic"] = False

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"success_status": True, "data": response["Item"]}),
        }

    except Exception as error:
        print(str(error))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps(
                {
                    "success_status": False,
                    "message": "Error while viewing the organisation",
                }
            ),
        }
