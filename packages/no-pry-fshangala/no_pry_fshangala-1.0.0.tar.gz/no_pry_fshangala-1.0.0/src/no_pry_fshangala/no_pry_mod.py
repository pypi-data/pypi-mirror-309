import base64
import argparse

class Credentials:
  def __init__(self,server:str,username:str,password:str):
    self.server=server
    self.username=username
    self.password=password
  
  def __str__(self):
    return f"{self.username}@{self.server}?password={self.password}"

class B64:
  def encrypt(self,credentials:Credentials)->str:
    enc_server=base64.b64encode(credentials.server.encode()).decode()
    enc_username=base64.b64encode(credentials.username.encode()).decode()
    enc_password=base64.b64encode(credentials.password.encode()).decode()
    token=f"b64.{enc_server}.{enc_username}.{enc_password}"
    return token
  
  def decrypt(tokens:list)->Credentials:
    if len(tokens) == 4:
      server=base64.b64decode(tokens[1]).decode()
      username=base64.b64decode(tokens[2]).decode()
      password=base64.b64decode(tokens[3]).decode()
      
      credentials=Credentials(server,username,password)
      return credentials
    else:
      raise Exception("Invalid token length")

def decrypt(token:str)->Credentials:
  tokens=token.split(".")
  if tokens[0] == "b64":
    crypt=B64()
    return crypt.decrypt(tokens)
  else:
    raise Exception("Invalid token type")

def encrypt(credentials:Credentials,ttype:str="b64")->str:
  if ttype == "b64":
    crypt=B64()
    return crypt.encrypt(credentials=credentials)
  else:
    raise Exception("Invalid token type")

def b64(args:argparse.Namespace)->str:
  server=base64.b64encode(args.server.encode()).decode()
  username=base64.b64encode(args.username.encode()).decode()
  password=base64.b64encode(args.password.encode()).decode()
  token=f"{args.type}.{server}.{username}.{password}"
  return token

def decryptb64(tokens:str)->Credentials:
  if len(tokens) == 4:
    server=base64.b64decode(tokens[1]).decode()
    username=base64.b64decode(tokens[2]).decode()
    password=base64.b64decode(tokens[3]).decode()
    
    credentials=Credentials(server,username,password)
    return credentials
  else:
    raise Exception("Invalid token length")