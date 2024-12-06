import base64
import argparse
import pandas

class Credentials:
  def __init__(self,server:str,username:str,password:str):
    self.server=str(server)
    self.username=str(username)
    self.password=str(password)
  
  def __str__(self):
    return f"{self.username}@{self.server}?password={self.password}"

class B64:
  def encrypt(self,credentials:Credentials)->str:
    enc_server=base64.b64encode(credentials.server.encode()).decode()
    enc_username=base64.b64encode(credentials.username.encode()).decode()
    enc_password=base64.b64encode(credentials.password.encode()).decode()
    token=f"b64.{enc_server}.{enc_username}.{enc_password}"
    return token
  
  def decrypt(self,tokens:list)->Credentials:
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

def encryptFile(path):
  df = pandas.read_csv(path)
  data = {
    "server":[],
    "code":[]
  }
  for i in df.index:
    code = encrypt(Credentials(server=df.loc[i,"server"],username=df.loc[i,"username"],password=df.loc[i,"password"]),ttype="b64")
    data["server"].append(df.loc[i,"server"])
    data["code"].append(code)
  dfout = pandas.DataFrame.from_dict(data=data)
  dfout.to_csv("encrypted.csv",index=False)
  print(dfout)

def decryptFile(path):
  df = pandas.read_csv(path)
  data={
    "server":[],
    "username":[],
    "password":[],
    "type":[],
  }
  for i in df.index:
    credentials=decrypt(df.loc[i,"code"])
    data["server"].append(credentials.server)
    data["username"].append(credentials.username)
    data["password"].append(credentials.password)
    data["type"].append("b64")
  dfout = pandas.DataFrame.from_dict(data=data)
  dfout.to_csv("decrypted.csv",index=False)
  print(dfout)

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