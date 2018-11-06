import os
from random import randint
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

key = "YELLOW SUBMARINE"
nonce = 0
block_size = 16

string = base64.b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")


