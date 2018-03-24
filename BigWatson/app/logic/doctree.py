import nltk.tokenize.punkt as punkt
import nltk.tokenize.moses as moses

sent_tokenizer = punkt.PunktSentenceTokenizer()
word_tokenizer = moses.MosesTokenizer(lang='en')
word_detokenizer = moses.MosesDetokenizer(lang='en')

class SentenceNode:
    def __init__(self, text, index_start, leading_whitespace=""):
        self.original_text = text
        self.index_start = index_start
        self.length = len(text)
        self.leading_whitespace = leading_whitespace
        self.word_nodes = []
        # Create word nodes
        head_index = index_start
        relative_offset = head_index.get()
        for word in word_tokenizer.tokenize(text):
            last = head_index.get() - relative_offset
            offset = text.index(word, last) - last
            node = WordNode(word, head_index.next(offset))
            self.word_nodes.append(node)
            head_index = node.index_end

        self.index_end = head_index

    def get_text(self):
        return ' '.join(word_detokenizer.detokenize([n.text for n in self.word_nodes]))

    def word_at(self, index):
        """ Returns the word (or whitespace) at the given document index.

            Performs a binary search on the child (word) nodes of this sentence for a node containing the given index.
            If the index lies in leading whitespace, the whitespace string will be returned.
        """
        return _binary_search_nodes(index, self.word_nodes)

    def delete(self, word):
        assert(word in self.word_nodes)
        arr_index = self.word_nodes.index(word)
        self.word_nodes.remove(word)
        if arr_index > 0:
            ind = min(arr_index, len(self.word_nodes) - 1)
            self.word_nodes[ind].reparent(self.word_nodes[ind - 1])
        elif len(self.word_nodes) > 0:
            self.word_nodes[0].index_start.offset = 0
            self.word_nodes[0].reparent(None)

        self.index_end = self.word_nodes[-1].index_end

    def delete_at(self, index):
        word = self.word_at(index)
        assert(word is not None)
        self.delete(word)

    def get_start_index(self):
        """Returns the integer document start index of this word node."""

        return self.index_start.get()

    def get_end_index(self):
        """Returns the integer document end index of this word node."""

        return self.index_end.get()


    def __repr__(self):
        return '{0}@[{1},{2}] | {3}'.format(self.get_text(), self.index_start, self.index_end, [w.__repr__() for w in self.word_nodes])


class WordNode:
    def __init__(self, text, index_start):
        self.text = text
        self.original_text = text
        self.index_start = index_start
        self.index_end = index_start.next(len(text))
        self.length = len(text)

    def get_start_index(self):
        """Returns the integer document start index of this word node."""

        return self.index_start.get()

    def get_end_index(self):
        """Returns the integer document end index of this word node."""

        return self.index_end.get()

    def update_text(self, new_text):
        """Updates the text and indices of this word node."""

        self.text = new_text
        self.index_end.offset = len(new_text)

    def reparent(self, new_parent):
        """Reparents the start index of this word node to the given word node."""
        assert(new_parent is None or isinstance(new_parent, WordNode))

        if new_parent is None:
            self.index_start.parent = None
            return

        self.index_start.parent = new_parent.index_end

    def __repr__(self):
        return '{0}@[{1},{2}]'.format(self.text, self.index_start, self.index_end)

class DocTree:
    """ Represents a fully indexed article as a tree of sentences and words.

        DocTree guarrantees that state changes will be propagated throughout the tree, i.e. deletion or update of a
        word will update all dependent word/sentence indices, etc.
    """

    def __init__(self, article):
        self.original_title = article.title
        self.original_summary = article.summary
        self.original_body = article.body
        self.title_node = SentenceNode(article.title, LinkedIndex(0))
        self.summary_nodes = self._sent_tokenize(self.original_summary)
        self.body_nodes = self._sent_tokenize(self.original_body)

    def body_sentence_at(self, index):
        """Returns the body sentence at the given document index."""

        return _binary_search_nodes(index, self.body_nodes)

    def summary_sentence_at(self, index):
        """Returns the summary sentence at the given document index."""

        return _binary_search_nodes(index, self.summary_nodes)

    def body_word_at(self, index):
        sentence = self.body_sentence_at(index)
        if sentence is None:
            return None
        return sentence.word_at(index)

    def summary_word_at(self, index):
        sentence = self.summary_sentence_at(index)
        if sentence is None:
            return None
        return sentence.word_at(index)

    def title_word_at(self, index):
        return self.title_node.word_at(index)

    def get_body(self):
        return ''.join([s.leading_whitespace + s.get_text() for s in self.body_nodes])

    def get_summary(self):
        return ''.join([s.leading_whitespace + s.get_text() for s in self.summary_nodes])

    def get_title(self):
        return self.title_node.get_text()

    def _sent_tokenize(self, raw_text):
        raw_index = 0
        head_index = None
        tokens = sent_tokenizer.tokenize(raw_text)
        nodes = []
        for token in tokens:
            raw_st_index = raw_text.index(token, raw_index)
            st_index = LinkedIndex(raw_st_index - raw_index, parent=head_index)
            leading_whitespace = raw_text[raw_index:raw_st_index]
            node = SentenceNode(token, st_index, leading_whitespace)
            nodes.append(node)
            head_index = node.index_end
            raw_index = raw_st_index + len(token)
        return nodes

    def __repr__(self):
        return '\n'.join(['{0}'.format(s) for s in self.summary_nodes + self.body_nodes])

def _binary_search_nodes(index, nodes):
    if len(nodes) == 0:
        return None
    mid = int(len(nodes) / 2)
    node = nodes[mid]
    index_end = node.get_end_index()
    index_start = index_end - node.length
    if index < index_end and index >= index_start:
        return node
    elif index >= index_end:
        return _binary_search_nodes(index, nodes[mid + 1:])
    else:
        return _binary_search_nodes(index, nodes[:mid])

class LinkedIndex:
    def __init__(self, offset, parent=None):
        self.offset = offset
        self.parent = parent

    def get(self):
        if self.parent is None:
            return self.offset
        return self.offset + self.parent.get()

    def next(self, offset):
        return LinkedIndex(offset, parent=self)

    def __repr__(self):
        return '{0}'.format(self.get())
