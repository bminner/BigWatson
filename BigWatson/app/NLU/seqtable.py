class SeqTable:
    def __init__(self, seqlist):
        self.seqs = []
        self.total_len = 0
        for seq in seqlist:
            self.seqs.append((seq, self.total_len))
            self.total_len += len(seq)

    def lookup(self, index):
        """Looks up the given index in the sequence table.

            Returns a 3-tuple of: the sequence s in which 'index' lies, the
            index of s in the parent sequence, and the relative location of
            'index' in s (index - start of s).
        """
        assert index >= 0
        assert index < self.total_len
        return self._lookup(index, self.seqs)

    def _lookup(self, index, seqs, offs=0):
        mid = int(len(seqs) / 2)
        seq, tlen = seqs[mid]
        if index < tlen:
            return self._lookup(index, seqs[:mid])
        elif index >= tlen + len(seq):
            return self._lookup(index, seqs[mid:], offs + mid)
        else:
            return seq, mid + offs, index - tlen
