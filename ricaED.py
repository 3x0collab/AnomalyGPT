
# Python program to demonstrate
# Substitution Cipher


import string

"""
create a dictionary to store the substitution
for the given alphabet in the plain text
based on the key
"""


class E():
    def __init__(self, kye="@adr0it", char_only=True):
        self.key = 7
        self.kye = kye
        # A list containing all characters
        self.all_letters = string.ascii_letters if char_only else string.digits + \
            string.ascii_letters

    def E(self, plain_txt):
        dict1 = {}
        plain_txt = self.kye + plain_txt

        for i in range(len(self.all_letters)):
            dict1[self.all_letters[i]] = self.all_letters[(
                i+self.key) % len(self.all_letters)]

        cipher_txt = []
        # loop to generate ciphertext

        for char in plain_txt:
            if char in self.all_letters:
                temp = dict1[char]
                cipher_txt.append(temp)
            else:
                temp = char
                cipher_txt.append(temp)

        cipher_txt = "".join(cipher_txt)
        return cipher_txt

    """
	create a dictionary to store the substitution
	for the given alphabet in the cipher
	text based on the key
	"""

    def D(self, cipher_txt):
        dict2 = {}
        for i in range(len(self.all_letters)):
            dict2[self.all_letters[i]] = self.all_letters[(
                i-self.key) % (len(self.all_letters))]
        # loop to recover plain text
        D_txt = []
        for char in cipher_txt:
            if char in self.all_letters:
                temp = dict2[char]
                D_txt.append(temp)
            else:
                temp = char
                D_txt.append(temp)

        D_txt = "".join(D_txt)
        # print("Recovered plain text :", D_txt.replace(self.kye,""))
        return D_txt.replace(self.kye, "")


if __name__ == '__main__':
    # E plain text
    en = E(char_only=False)
    # D cipher text
    e = en.E('Rica1')
    print('E: ', e)
    d = E(char_only=False).D(e)
    print('D: ', d)
