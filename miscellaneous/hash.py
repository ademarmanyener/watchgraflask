# -*- encoding: utf-8 -*-

# this program is written to
# hash and verify strings
# it can be used for passwords
# if you really want to do that

# it uses passlib.sha256_crypt

from passlib.hash import sha256_crypt 

def hash_str_hash(get_str): return sha256_crypt.hash(get_str)

def hash_str_verify(get_answ, get_hashed_str): return sha256_crypt.verify(get_answ, get_hashed_str) 

class MainApplication:
    def __init__(self):
        print("1 - Hash")
        print("2 - Verify")
        _ = int(input('Seçenek: '))
        if _ == 1:
            __ = str(input("String: "))
            print(hash_str_hash(__))
        if _ == 2:
            __1 = str(input("String: "))
            __2 = str(input("Hashed: "))
            print(hash_str_verify(__1, __2))

if __name__ == '__main__': app = MainApplication()
