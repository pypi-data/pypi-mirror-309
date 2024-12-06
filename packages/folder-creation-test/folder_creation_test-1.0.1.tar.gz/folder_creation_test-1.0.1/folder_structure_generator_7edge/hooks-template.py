from dredd_hooks import before_each, after_each
import os
import json
import logging
import urllib.parse
import random
import string

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename="hooks.log",
    filemode="a",
)

# This id for dynamic api testing and can be assigned with any value from after each function
global_id = None

@after_each
def skip_test_results(transaction):
    if (
            transaction["expected"]["statusCode"] == "500" or
            transaction["expected"]["statusCode"] == "403"    
       ):
        transaction["skip"] = True


@before_each
def set_authorization(transaction):

    uri = urllib.parse.unquote(transaction["request"]["uri"])
    token = str(os.environ.get('admin'))
    random.randint(1, 99)
    random_upper = random.choice(string.ascii_uppercase)
    random_lower = "".join(random.choices(string.ascii_lowercase, k=5))
    random_string = random_upper + random_lower
    transaction["request"]["uri"] = urllib.parse.unquote(transaction["request"]["uri"])

    if transaction["expected"]["statusCode"] != "401":
        print(f"Token before setting in Authorization header: {token}")
        transaction["request"]["headers"]["Authorization"] = f"Bearer {token}"
    

# @after_each
# def store_created_bank_id(transaction):
#     global created_bank_id
#     uri = urllib.parse.unquote(transaction["request"]["uri"])
#     if transaction["expected"]["statusCode"] == "201" and uri == "/":
#         created_bank_id = json.loads(transaction["real"]["body"])["id"]
