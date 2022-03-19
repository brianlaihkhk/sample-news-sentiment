import jwt
import yaml
import sys

def encrypt(file_name):
    if not input:
        raise Exception("Environment file is required as input. Usage : ./encrypt_string.py <File path>")

    with open(file_name, "r") as stream:
        try:
            env = yaml.safe_load(stream)
            env = convert(env["web"]["environment"])
            
            key = env["RDS_ENCRYPT_KEY"]
            db_username = env["RDS_USERNAME"]
            db_password = env["RDS_PASSWORD"]

            if not env["RDS_ENCRYPT_KEY"]:
                raise Exception("RDS_ENCRYPT_KEY is empty")
            if not env["RDS_USERNAME"]:
                raise Exception("RDS_USERNAME is empty")
            if not env["RDS_PASSWORD"]:
                raise Exception("RDS_PASSWORD is empty")  

            print("- RDS_USERNAME=" + jwt.encode({"body" : db_username}, key))
            print("- RDS_PASSWORD=" + jwt.encode({"body" : db_password}, key))
        except yaml.YAMLError as exc:
            print(exc)

def convert(input):
    output = {}
    for i in range(0, len(input)):
        split = input[i].split("=")
        output = {**output, split[0]: split[1]}
    return output

if __name__ == "__main__":
   encrypt(sys.argv[1])