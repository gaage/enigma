class CipherTabelle(object):
    """
    This class selects a set of cipher tables from the original set
    of the enigma. The selection is done by manipulating data from
    the datestring of the day the message was encoded.
    """

    walzen = [
            # 'i' : 1930 : Enigma I
            'EKMFLGDQVZNTOWYHXUSPAIBRCJ',

            # 'ii' : 1930 : Enigma I
            'AJDKSIRUXBLHWTMCQGZNPYFVOE',

            # 'iii' : 1930 : Enigma I
            'BDFHJLCPRTXVZNYEIWGAKMUSQO',

            # 'iv' : December 1938 : M3 Army
            'ESOVPZJAYQUIRHXLNFTGKDCMWB',

            # 'v' : December 1938 : M3 Army
            'VZBRGITYUPSDNHLXAWMJQOFECK',

            # 'vi' : 1939 : M3 & M4 Naval (FEB 1942)
            'JPGVOUMFYQBENHZRDKASXLICTW',

            # 'vii' : 1939 : M3 & M4 Naval (FEB 1942)
            'NZJHGRCXMYSWBOUFAIVLPEKQDT',

            # 'viii' : 1939 : M3 & M4 Naval (FEB 1942)
            'FKQHTLXOCBJSPDZRAMEWNIUYGV',

            # 'beta' : Spring 1941 : M4 R2
            'LEYJVCNIXWPBQMDRTAKZGFUHOS',

            # 'gamma' : Spring 1942 : M4 R2
            'FSOKANUERHMBTIYCWLQPZXVGJD',
    ]

    umkehrs_walzen = [
            # 'a'
            'EJMZALYXVBWFCRQUONTSPIKHGD',

            # 'b'
            'YRUHQSLDPXNGOKMIEBFZCWVJAT',

            # 'c'
            'FVPJIAOYEDRZXWGCTKUQSBNMHL',

            # 'bt' : 1940 : M4 R1 (M3 + Thin)
            'ENKQAUYWJICOPBLMDXZVFTHRGS',

            # 'ct' : 1940 : M4 R1 (M3 + Thin)
            'RDOBJNTKVEHMLFCWZAXGYIPSUQ',
    ]

    def __init__(self, anzahl_walze, samen):

        self.anzahl_walze = anzahl_walze


        import random
        random.seed(a=samen)
        self.walze_id = []
        self.walze_ausg = []
        self.walze_ringst = []

        # Select walzes and init positions using random fn
        self.umkwz_id = random.randrange(5)

        for w in range(self.anzahl_walze):
            self.walze_id.append(random.randrange(10))
            self.walze_ausg.append(random.randrange(26))
            self.walze_ringst.append(random.randrange(26))

    def __str__(self):
        return "{} {} {} {}".format(
                         self.umkwz_id,
                         self.walze_id,
                         self.walze_ausg,
                         self.walze_ringst)

