from .rsa import urlsafe_decrypt as rsa_urlsafe_decrypt
from .rsa import urlsafe_encrypt as rsa_urlsafe_encrypt
from .aes import urlsafe_decrypt as aes_urlsafe_decrypt
from .aes import urlsafe_encrypt as aes_urlsafe_encrypt
import json
import base64


from Crypto.Random import get_random_bytes

from .aes import encrypt as aes_encrypt
from .aes import decrypt as aes_decrypt
from .rsa import encrypt as rsa_encrypt
from .rsa import decrypt as rsa_decrypt


def main():
    key = get_random_bytes(16)
    binary_private_key = open('private_recipient_key.pem').read()
    binary_public_key = open('public_recipient_key.pub').read()

    # data to scrypt
    secrets = {
        'login': '',
        'password': '',
        'email': '',
    }

    msg_to_encrypt = json.dumps(secrets)

    # encrypt data with AES
    nonce, tag, ciphertext = aes_encrypt(msg_to_encrypt, key)

    # encrypt AES key with RSA
    aes_keys = base64.urlsafe_b64encode(key + nonce + tag)
    encrypted_key = rsa_encrypt(data=aes_keys,
                                binary_public_key=binary_public_key)

    # save or send payload
    payload = {
        'ciphertext': ciphertext,
        'encrypted_key': encrypted_key
    }

    # decrypt key with rsa
    encrypted_key = payload['encrypted_key']
    decrypted_key = rsa_decrypt(
        encrypted_data=encrypted_key, binary_private_key=binary_private_key)
    secret = base64.urlsafe_b64decode(decrypted_key)
    d_key = secret[:16]
    d_nonce = secret[16:32]
    d_tag = secret[32:]

    print(d_key == key, d_nonce == nonce, d_tag == tag)

    # decrypt
    plaintext = aes_decrypt(ciphertext, key, nonce, tag)
    out_secrets = json.loads(plaintext)
    print(out_secrets)


# main()


def test_encrypt_credentials():
    key = get_random_bytes(16)
    binary_private_key = open('../certs/private_recipient_key.pem').read()
    binary_public_key = open('../certs/public_recipient_key.pub').read()

    login = 'fulano'
    password = 'secret'
    email = 'email@test.com'

    s_login = aes_urlsafe_encrypt(login, key)
    s_password = aes_urlsafe_encrypt(password, key)
    s_email = aes_urlsafe_encrypt(email, key)
    s_key = rsa_urlsafe_encrypt(key, binary_private_key)

    print({
        'login': s_login,
        'password': s_password,
        'email': s_email,
        'encrypted_key': s_key,
    })

    secret = aes_urlsafe_encrypt(login, key)
    print(aes_urlsafe_decrypt(secret, key))


test_encrypt_credentials()
