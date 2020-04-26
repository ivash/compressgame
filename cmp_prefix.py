from huffman import HuffmanEncoder
from binary_tools import BitBuffer

class Compressor:
    r'''Strategy:
        1. Figure out how much each word has in common with the previous.
           For example, "apple" followed by "apples" has 5 letters in common.
           We can encode "apples" as (5, "s"), meaning, repeat 5 letters from
           the previous word, then append "s".
        2. Use Huffman encoding on the common-letter counts.
        3. Use Huffman encoding on the tail part of each word.
    '''
    def Name(self):
        return 'prefix'

    def Compress(self, words):
        repeatRoot, tailRoot, charRoot = self._HuffmanCodes(words)
        repeatCode = repeatRoot.MakeEncoding()
        tailCode = tailRoot.MakeEncoding()
        charCode = charRoot.MakeEncoding()
        buf = self._Encode(words, repeatCode, tailCode, charCode)
        source = "Repeat=" + repeatRoot.SourceCode() + "\n"
        source += "Tail=" + tailRoot.SourceCode() + "\n"
        source += "Char=" + charRoot.SourceCode() + "\n"
        source += "NumWords={:d}\n".format(len(words))
        source += "Bits=r'''\n" + buf.Format() + "'''\n"
        return source

    def _Encode(self, words, repeatCode, tailCode, charCode):
        pw = ''
        buf = BitBuffer()
        for w in words:
            prefix = self._LettersInCommon(pw, w)
            buf.Append(repeatCode[prefix])
            tail = w[prefix:]
            buf.Append(tailCode[len(tail)])
            for c in tail:
                buf.Append(charCode[c])
            pw = w
        return buf

    def _HuffmanCodes(self, words):
        repeatHuff = HuffmanEncoder()
        tailHuff = HuffmanEncoder()
        charHuff = HuffmanEncoder()
        pw = ''
        for w in words:
            prefix = self._LettersInCommon(pw, w)
            repeatHuff.Tally(prefix)
            tailHuff.Tally(len(w) - prefix)
            for c in w[prefix:]:
                charHuff.Tally(c)
            pw = w
        return repeatHuff.Compile(), tailHuff.Compile(), charHuff.Compile()

    def _LettersInCommon(self, a, b):
        n = min(len(a), len(b))
        for i in range(n):
            if a[i] != b[i]:
                return i
        return n

