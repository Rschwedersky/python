import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt(data, key):
    '''
    encrypt return the cipher text form, nonce and tag, of a plain text for a given key.
    '''

    data = str.encode(data)

    cipher  = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    return cipher.nonce, tag, ciphertext

def decrypt(ciphertext, key, nonce, tag):
    '''
    decrypt return the plain text form of a cipher text for a given key, nonce, and tag.
    '''
    cipher  = AES.new(key, AES.MODE_EAX, nonce)
    data    = cipher.decrypt_and_verify(ciphertext, tag)
    return data



def urlsafe_encrypt(data:str, key:bytes) -> str:
    '''
    encrypt data using AES and return a token in format "nonce.tag.encrypted"
    '''
    nonce, tag, encrypted_data = encrypt(data, key)
    s_nonce =  base64.urlsafe_b64encode(nonce).decode('utf-8')
    s_tag   =  base64.urlsafe_b64encode(tag).decode('utf-8')
    s_encrypted_data   =  base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
    
    return f"{s_nonce}:{s_tag}:{s_encrypted_data}"


def urlsafe_decrypt(data: str, key: bytes):
    '''
    receive a base64 urlsafe token in format "nonce.tag.encrypted" end decrypt AES the plain text
    '''
    s_nonce, s_tag, s_encrypted_data = data.split(":")

    nonce =  base64.urlsafe_b64decode(s_nonce)
    tag   =  base64.urlsafe_b64decode(s_tag)
    encrypted_data   =  base64.urlsafe_b64decode(s_encrypted_data)

    plain_text = decrypt(encrypted_data, key, nonce, tag).decode('utf-8')
    return plain_text