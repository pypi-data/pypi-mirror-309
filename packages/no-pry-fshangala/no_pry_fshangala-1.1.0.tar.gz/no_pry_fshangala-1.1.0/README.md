# No Pry
A python module to encrypt and decript passwords and usernames

# Usage

## Commandline program

### Encrypting credentials

Example credentials

|Sever|Username|Password|
|-----|--------|--------|
|localhost|root|1234|

```bash
no_pry -s localhost -u root -p 1234
```

This generates a token encrypted in base64

### Decrypting token

Example token: `b64.bG9jYWxob3N0.cm9vdA==.MTIzNA==`

```bash
no_pry -d b64.bG9jYWxob3N0.cm9vdA==.MTIzNA==
```

This decrypts the token and gives credentials

## Module

### Installation

```bash
pip install no_pry_fshangala
```

Example script

```python
# import modules
import argparse
from no_pry_fshangala import no_pry_mod

# parse arguments
parser=argparse.ArgumentParser(
  prog="no_pry",
  description="Encrypts login credentials",
)
parser.add_argument("-s","--server",required=True)
parser.add_argument("-u","--username",required=True)
parser.add_argument("-p","--password",required=True)
parser.add_argument("-t","--type",default="b64",choices=["b64"])
args=parser.parse_args()

if args.type == "b64":
  # create a credentials object
  credentials=no_pry_mod.Credentials(server=args.server,username=args.username,password=args.password)
  # create the encryption object
  crypt=no_pry_mod.B64()
  # encrypt the credentials object
  token=crypt.encrypt(credentials=credentials)
  # print the resulting token
  print(token)
```
