import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def encrypt(data, binary_public_key):
    public_key = RSA.importKey(binary_public_key)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher_rsa.encrypt(data)
    return encrypted_data


def decrypt(encrypted_data, binary_private_key):
    private_key = RSA.importKey(binary_private_key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher_rsa.decrypt(encrypted_data)
    return decrypted_data


def urlsafe_encrypt(data:str, key:bytes) -> str:
    '''
    encrypt data using RSA and return a token in base64 format
    '''
    encrypted_data = encrypt(data, key)
    s_encrypted_data   =  base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
    
    return s_encrypted_data


def urlsafe_decrypt(data: str, key: bytes):
    '''
    decode base64 and decrypt RSA
    '''
    encrypted_data   =  base64.urlsafe_b64decode(data)

    plain_text = decrypt(encrypted_data, key)
    return plain_text