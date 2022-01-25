# -*- encoding: utf-8 -*-

# KeyGen.py -> A simple CD Key Generator, written in python.

import random, string

def get_keygen(characters=string.ascii_uppercase + string.digits):
    return '-'.join(''.join(random.choice(characters) for _ in range(5)) for _ in range(5))

class MainApplication:
    def __init__(self):
        global i
        count = int(input("Oluşturulmak istenen anahtar miktarı nedir? "))
        print("")
        for i in range(count): print('\t\t ' + str(i) + ' - ' + get_keygen())
        print("\n{} tane anahtar oluşturuldu.".format(count))

if __name__ == '__main__': app = MainApplication()
