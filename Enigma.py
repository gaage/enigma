# Helper functions
def zi(zeichen):
    """
    Character index: zeichen index
    """
    return ord(zeichen) - ord('A')


def ruckwarts_rechnen(walze):
    """
    Compute the table for inverse transformation through a rotor (walze)
    """
    from string import ascii_uppercase
    lst_inv = [None]*26
    for f, a in zip(walze, ascii_uppercase):
        lst_inv[zi(f)] = a
    return lst_inv


def rotieren(wal, s):
    """
    Rotate a walze s schritte
    """
    return wal[s:] + wal[:s]


class EnigmaMachine(object):

    def __init__(self, cipher):
        walze_id = cipher.walze_id
        walze_ausg = cipher.walze_ausg
        walze_ringst = cipher.walze_ringst

        # Initialize rotor objects
        self.walzen = []
        for w, a, r in zip(walze_id, walze_ausg, walze_ringst):
            wl = Walze(cipher.walzen[w])
            wl.insertieren_als(a, r)
            self.walzen.append(wl)

        # Initialize reflektor object
        umkwz = cipher.umkehrs_walzen[cipher.umkwz_id]
        self.umkehrs_walze = UmkehrsWalze(spiegel=umkwz)
        self.klar_text = ''
        self.geheim_text = ''

    def eingabe(self, text):
        """
        Filter by converting to upper case and removing whitespace
        Illegal characters (non-alpha a-zA-Z) gives error
        Note: Filtered-out whitespace will not re-appear in decoded
        output.
        """
        klar_text = ''
        for n, m in [(zi(m.upper()), m.upper()) for m in text]:
            if m == ' ':
                continue
            elif (n < 0) or (n > 25):
                print('Zeichen {:s} nicht gestattet'.format(m))
                continue
            else:
                klar_text += m
        self.klar_text = klar_text

    def ausfuhren(self):
        """
        Run a string of characters through the enigma loop
        For each character, propagate the rotor machinery
        """
        ausgabe = ''
        for zeichen in self.klar_text:
            ausgabe += self.zeichen_kodung(zeichen)
            self.propagieren()
        self.geheim_text = ausgabe

    def grund_stellung(self):
        """
        Reset rotors to starting position
        """
        for position in range(3):
            self.walzen[position].grund_stellung()

    def zeichen_kodung(self, zeichen):
        """
        Encode a character by passiing it forth and back through the rotors
        """
        z = zeichen
        for n in range(len(self.walzen)-1, -1, -1):
            z = self.walzen[n].rechts_links(z)
        z = self.umkehrs_walze.spiegelen(z)
        for n in range(len(self.walzen)):
            z = self.walzen[n].links_rechts(z)
        return z

    def propagieren(self):
        """
        Advance rotors according to ring_stellung setting
        """
        if self.walzen[1].bei_ringstellung():
            self.walzen[0].wende(1)
        if self.walzen[2].bei_ringstellung():
            self.walzen[1].wende(1)
        self.walzen[2].wende(1)

    def ausgabe(self, text):
        """
        Print the given text enigma-style
        """
        block = 0
        block_size = 5
        columns = 8

        while True:
            if len(text) > block_size:
                print(text[:block_size] + ' ', end='')
                text = text[block_size:]
                block += 1
            else:
                print(text)
                break

            if block >= columns:
                print('')
                block = 0


class UmkehrsWalze(object):
    """
    Model the reflector object
    """

    def __init__(self, spiegel):
        # Assign reflector forward substitutions
        self.spiegel = spiegel

    def spiegelen(self, inp):
        return self.spiegel[zi(inp)]


class Walze(object):
    """
    Model the rotor object
    """

    def __init__(self, rechts_ersetzen):
        """
        Assign rotor forward substitutions
        Convert string to list of characters
        """
        self.rechts_ersetzen = list(rechts_ersetzen)

    def insertieren_als(self, ausg_position, ring_stellung):
        """
        Setup a rotor object with an initial position and
        it's given carry position
        """
        # Set rotor's carry position
        self.ring_stellung = chr(ring_stellung + ord('A'))
        # Turn rotor to given initial position (integer)
        self.wende(ausg_position)
        # Calculate the inverse substitution of this setting
        self.links_ersetzen = ruckwarts_rechnen(self.rechts_ersetzen)
        # Remember rotor's insertieren_als for later reset (grund_stellung)
        self.rechts_ersetzen_ausgang = self.rechts_ersetzen
        self.links_ersetzen_ausgang = self.links_ersetzen

    def rechts_links(self, rechts):
        """
        Transform a character input on the right side of a rotor
        to its value on the left side
        """
        return self.rechts_ersetzen[zi(rechts)]

    def links_rechts(self, links):
        """
        Transform a character input on the left side of a rotor
        to its value on the right side
        """
        return self.links_ersetzen[zi(links)]

    def grund_stellung(self):
        """
        Reset rotors to starting position
        """
        self.rechts_ersetzen = self.rechts_ersetzen_ausgang
        self.links_ersetzen = self.links_ersetzen_ausgang

    def wende(self, schritte):
        """
        Turn a rotor the given number of steps
        Compute a new inverse rotor using ruckwarts_rechnen
        """
        w = self.rechts_ersetzen
        if schritte > 0:
            w = rotieren(w, schritte)
            wr = ruckwarts_rechnen(w)
            self.rechts_ersetzen = w
            self.links_ersetzen = wr

    def bei_ringstellung(self):
        """
        True if rotor is at the carry position, and will promote
        the next rotor (if present) at the next cycle
        """
        return self.rechts_ersetzen[0] == self.ring_stellung
