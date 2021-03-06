class BitReader:
    def __init__(self, encoded):
        self.encoded = encoded.replace('\n', '')
        self.position = 0
        self.accum = 0
        self.nbits = 0

    def GetNextBit(self):
        if self.nbits == 0:
            c = self.encoded[self.position]
            self.position += 1
            self.accum = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'.index(c)
            self.nbits = 6
        bit = 1 & (self.accum >> 5)
        self.accum = 0b111111 & (self.accum << 1)
        self.nbits -= 1
        return bit

def Huffman(reader, node):
    while isinstance(node, tuple):
        node = node[reader.GetNextBit()]
    return node

def Expand():
    reader = BitReader(Bits)
    pw = ''
    wlist = []
    for w in range(NumWords):
        repeatLen = Huffman(reader, Repeat)
        tailLen = Huffman(reader, Tail)
        if repeatLen == 0:
            i = 0
        else:
            i = ord(pw[repeatLen-1]) - ord('`')
        w = pw[:repeatLen]
        for _ in range(tailLen):
            c = Huffman(reader, Char[i])
            w += c
            i = ord(c) - ord('`')
        wlist.append(w)
        pw = w
    return '\n'.join(wlist)
