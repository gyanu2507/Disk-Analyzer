import hashlib

def calculate_md5(file_path, block_size=65536):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(block_size)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()



# md5_calculate = lambda x: hashlib.md5(x).hexdigest()
# sha1_calculate = lambda x: hashlib.sha1(x).hexdigest()
# sha256_calculate = lambda x: hashlib.sha256(x).hexdigest()
# sha512_calculate = lambda x: hashlib.sha512(x).hexdigest()
# sha3_256_calculate = lambda x: hashlib.sha3_256(x).hexdigest()
# sha3_512_calculate = lambda x: hashlib.sha3_512(x).hexdigest()
# blake2b_calculate = lambda x: hashlib.blake2b(x).hexdigest()
# blake2s_calculate = lambda x: hashlib.blake2s(x).hexdigest()