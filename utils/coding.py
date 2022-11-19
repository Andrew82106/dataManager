from Crypto.Cipher import AES
import base64
import time


class Hash:
    def __init__(self):
        self.key = str(time.time_ns())[:16]
        self.BLOCK_SIZE = 16  # Bytes
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * \
                        chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]
        self.vi = '0102030405060708'

    def En(self, data__):
        data__ = self.pad(data__)
        cipher = AES.new(self.key.encode('utf8'), AES.MODE_CBC, self.vi.encode('utf8'))
        encryptedbytes = cipher.encrypt(data__.encode('utf8'))
        encodestrs = base64.b64encode(encryptedbytes)
        enctext = encodestrs.decode('utf8')
        return enctext

    def De(self, data__):
        data__ = data__.encode('utf8')
        encodebytes = base64.decodebytes(data__)
        cipher = AES.new(self.key.encode('utf8'), AES.MODE_CBC, self.vi.encode('utf8'))
        text_decrypted = cipher.decrypt(encodebytes)
        text_decrypted = self.unpad(text_decrypted)
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted


if __name__ == '__main__':
    data = 'herqvish acorn'
    X = Hash()
    z = X.En(data)
    print(X.De(z))

