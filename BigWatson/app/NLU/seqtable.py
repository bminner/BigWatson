class SeqTable:
    def __init__(self, seqlist):
        self.seqs = []
        self.total_len = 0
        for seq in seqlist:
            seqs.append((seq, self.total_len))
            self.total_len += len(seq)

    def lookup(self, index):
        """Returns the sequence in the table in which the given index lies."""
        return self._lookup(index, self.seqs)

    def _lookup(self, index, seqs):
        mid = len(seqs) / 2
        seq, tlen = seqs[mid]
        if index < tlen:
            return self._lookup(index, seqs[:mid])
        elif index >= tlen + len(seq):
            return self._lookup(index, seqs[mid:])
        else:
            return seq
