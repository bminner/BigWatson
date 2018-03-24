from ..logic.doctree import LinkedIndex, DocTree
from ..models.Article import Article
from django.test import TestCase

class DocTreeTest(TestCase):

    def test_doctree_init(self):
        article = Article(
            title='Test title',
            summary='Test summary',
            body='Do not go gentle into that good night. Rage, rage against the dying of the light.')
        doctree = DocTree(article)
        title_node = doctree.title_node
        summary_nodes = doctree.summary_nodes
        body_nodes = doctree.body_nodes
        self.assertEqual(title_node.get_text(), 'Test title')
        self.assertEqual(summary_nodes[0].get_text(), 'Test summary')
        self.assertEqual(summary_nodes[0].word_nodes[0].text, 'Test')
        self.assertEqual(summary_nodes[0].word_nodes[1].text, 'summary')
        self.assertEqual(body_nodes[0].get_text(), 'Do not go gentle into that good night.')
        self.assertEqual(body_nodes[1].get_text(), 'Rage, rage against the dying of the light.')
        self.assertEqual(len(body_nodes[0].word_nodes), 9)
        self.assertEqual(len(body_nodes[1].word_nodes), 10)

    def test_doctree_reconstruct_whitespace(self):
        article = Article(
            title='Test title',
            summary='Test summary',
            body='Do not go gentle into that good night.     \n\n Rage, rage against the dying of the light.')
        doctree = DocTree(article)
        self.assertEquals(article.body, doctree.get_body())

    def test_doctree_reconstruct_whitespace_after_edits(self):
        article = Article(
            title='Test title',
            summary='Test summary',
            body='Do not go gentle into that good night.     \n\n Rage, rage against the dying of the light.')
        doctree = DocTree(article)
        doctree.body_nodes[1].delete_at(50)
        doctree.body_nodes[0].word_nodes[3].update_text('forth')
        self.assertEquals('Do not go forth into that good night.     \n\n Rage rage against the dying of the light.', doctree.get_body())

    def test_doctree_lookup_body(self):
        article = Article(
            title='Test title',
            summary='Test summary',
            body='Do not go gentle into that good night. Rage, rage against the dying of the light.')
        doctree = DocTree(article)
        lookup_index_1 = 10
        lookup_index_2 = 48
        sentence_1 = doctree.body_sentence_at(lookup_index_1)
        sentence_2 = doctree.body_sentence_at(lookup_index_2)
        self.assertIsNotNone(sentence_1)
        self.assertIsNotNone(sentence_2)
        self.assertEquals(sentence_1.get_text(), 'Do not go gentle into that good night.')
        self.assertEquals(sentence_2.get_text(), 'Rage, rage against the dying of the light.')
        word_1 = sentence_1.word_at(lookup_index_1)
        word_2 = sentence_2.word_at(lookup_index_2)
        self.assertIsNotNone(word_1)
        self.assertIsNotNone(word_2)
        self.assertEquals(word_1.text, 'gentle')
        self.assertEquals(word_2.text, 'rage')

    def test_doctree_lookup_body_after_update(self):
        article = Article(
            title='Test title',
            summary='Test summary',
            body='Do not go gentle into that good night. Rage, rage against the dying of the light.')
        doctree = DocTree(article)
        lookup_index_1 = 15
        lookup_index_2 = 20
        sentence = doctree.body_sentence_at(lookup_index_1)
        word_1 = sentence.word_at(lookup_index_1)
        word_2 = sentence.word_at(lookup_index_2)
        self.assertEquals(word_1.text, 'gentle')
        self.assertEquals(word_2.text, 'into')
        word_1.update_text('lo')
        self.assertEquals(word_2.get_start_index(), 13)
        self.assertEquals(sentence.word_at(lookup_index_2).text, 'that')

    def test_doctree_lookup_body_after_deletion(self):
        article = Article(
            title='Test title',
            summary='Test summary',
            body='Do not go gentle into that good night. Rage, rage against the dying of the light.')
        doctree = DocTree(article)
        lookup_index_1 = 15
        lookup_index_2 = 23
        sentence = doctree.body_sentence_at(lookup_index_1)
        word_1 = sentence.word_at(lookup_index_1)
        word_2 = sentence.word_at(lookup_index_2)
        self.assertEquals(word_1.text, 'gentle')
        self.assertEquals(word_2.text, 'that')
        sentence.delete(word_1)
        self.assertEquals(sentence.get_text(), 'Do not go into that good night.')
        self.assertEquals(word_2.get_start_index(), 15)
        self.assertEquals(sentence.word_at(lookup_index_2).text, 'good')

    def test_doctree_delete_first_word(self):
        article = Article(
            title='Test title',
            summary='Test summary',
            body='Do not go gentle into that good night. Rage, rage against the dying of the light.')
        doctree = DocTree(article)
        lookup_index = 0
        sentence = doctree.body_sentence_at(lookup_index)
        word = sentence.word_at(lookup_index)
        self.assertEquals(word.text, 'Do')
        sentence.delete(word)
        self.assertEquals(sentence.get_text(), 'not go gentle into that good night.')
        self.assertEquals(sentence.word_nodes[0].get_start_index(), 0)

    def test_doctree_delete_last_word(self):
        article = Article(
            title='Test title',
            summary='Test summary',
            body='Do not go gentle into that good night. Rage, rage against the dying of the light.')
        doctree = DocTree(article)
        lookup_index = len(article.body) - 1
        sentence = doctree.body_sentence_at(lookup_index)
        end_index = sentence.get_end_index()
        word = sentence.word_at(lookup_index)
        self.assertEquals(word.text, '.')
        sentence.delete(word)
        self.assertEquals(sentence.get_text(), 'Rage, rage against the dying of the light')
        self.assertEquals(sentence.get_end_index(), end_index - 1)

class LinkedIndexTest(TestCase):

    def test_linked_index(self):
        index_0 = LinkedIndex(0)
        index_1 = LinkedIndex(4, parent=index_0)
        index_2 = LinkedIndex(5, parent=index_1)
        self.assertEqual(index_2.get(), 9)
        self.assertEqual(index_1.get(), 4)
        index_1.offset = 2
        self.assertEqual(index_2.get(), 7)
