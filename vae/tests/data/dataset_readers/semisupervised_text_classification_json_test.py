# pylint: disable=no-self-use,invalid-name
import string
import re
import numpy as np
from allennlp.common.util import ensure_list
from allennlp.common.util import prepare_environment
from allennlp.common.params import Params
from vae.data.dataset_readers import SemiSupervisedTextClassificationJsonReader
from vae.common.testing.test_case import VAETestCase


class TestTextClassificationJsonReader(VAETestCase):

    def test_read_from_file(self):
        reader = SemiSupervisedTextClassificationJsonReader()
        ag_path = self.FIXTURES_ROOT / "imdb" / "train.jsonl"
        instances = reader.read(ag_path)
        instances = ensure_list(instances)

        instance1 = {"tokens": ['...', 'And', 'I', 'never', 'thought', 'a', 'movie', 'deserved', 'to',
                                'be', 'awarded', 'a', '1', '!', 'But', 'this', 'one', 'is', 'honestly',
                                'the', 'worst', 'movie',
                                'I', "'ve", 'ever', 'watched', '.', 'My', 'wife', 'picked', 'it', 'up',
                                'because', 'of', 'the', 'cast', ',',
                                'but', 'the', 'storyline', 'right', 'since', 'the', 'DVD', 'box',
                                'seemed', 'quite',
                                'predictable', '.', 'It', 'is', 'not', 'a', 'mystery', ',', 'nor',
                                'a', 'juvenile',
                                '-', 'catching', 'film', '.', 'It', 'does', 'not', 'include', 'any',
                                'sensuality',
                                ',', 'if', 'that', "'s", 'what', 'the', 'title', 'could', 'remotely',
                                'have', 'suggest',
                                'any', 'of', 'you', '.', 'This', 'is', 'just', 'a', 'total', 'no', '-',
                                'no', '.',
                                'Do', "n't", 'waste', 'your', 'time', 'or', 'money', 'unless', 'you',
                                'feel', 'like',
                                'watching', 'a', 'bunch', 'of', 'youngsters', 'in', 'a', 'as',
                                '-', 'grown', '-', 'up',
                                'kind', 'of', 'Gothic', 'setting', ',', 'where', 'a', 'killer',
                                'is', 'going', 'after',
                                'them', '.', 'Nothing', 'new', ',', 'nothing', 'interesting', ',',
                                'nothing', 'worth',
                                'watching', '.', 'Max', 'Makowski', 'makes', 'the', 'worst', 'of',
                                'Nick', 'Stahl', '.'],
                     "label": "neg"}
        instance2 = {"tokens": ['The', 'fight', 'scenes', 'were', 'great', '.', 'Loved', 'the',
                                'old', 'and', 'newer',
                                'cylons', 'and', 'how', 'they', 'painted', 'the', 'ones', 'on',
                                'their', 'side', '.', 'It',
                                'was', 'the', 'ending', 'that', 'I', 'hated', '.', 'I', 'was',
                                'disappointed', 'that', 'it',
                                'was', 'earth', 'but', '150k', 'years', 'back', '.', 'But', 'to',
                                'travel', 'all', 'that',
                                'way', 'just', 'to', 'start', 'over', '?', 'Are', 'you', 'kidding',
                                'me', '?', '38k', 'people',
                                'that', 'fought', 'for', 'their', 'very', 'existence', 'and', 'once',
                                'they', 'get', 'to',
                                'paradise', ',', 'they', 'abandon', 'technology', '?', 'No',
                                'way', '.', 'Sure', 'they',
                                'were', 'eating', 'paper', 'and', 'rationing', 'food', ',',
                                'but', 'that', 'is', 'over',
                                '.', 'They', 'can', 'live', 'like', 'humans', 'again', '.',
                                'They', 'only', 'have', 'one',
                                'good', 'doctor', '.', 'What', 'are', 'they', 'going', 'to', 'do',
                                'when', 'someone', 'has',
                                'a', 'tooth', 'ache', 'never', 'mind', 'giving', 'birth', '...',
                                'yea', 'right', '.',
                                'No', 'one', 'would', 'have', 'made', 'that', 'choice', '.'],
                     "label": "pos"}
        instance3 = {"tokens": ['The', 'only', 'way', 'this', 'is', 'a', 'family', 'drama', 'is',
                                'if', 'parents', 'explain',
                                'everything', 'wrong', 'with', 'its', 'message.<br', '/><br',
                                '/>SPOILER', ':', 'they', 'feed',
                                'a', 'deer', 'for', 'a', 'year', 'and', 'then', 'kill', 'it',
                                'for', 'eating', 'their', 'food',
                                'after', 'killing', 'its', 'mother', 'and', 'at', 'first',
                                'pontificating', 'about', 'taking',
                                'responsibility', 'for', 'their', 'actions', '.', 'They', 'blame',
                                'bears', 'and', 'deer',
                                'for', '"', 'misbehaving', '"', 'by', 'eating', 'while', 'they',
                                'take', 'no', 'responsibility',
                                'to', 'use', 'adequate', 'locks', 'and', 'fences', 'or', 'even',
                                'learn', 'to', 'shoot',
                                'instead', 'of', 'twice', 'maiming', 'animals', 'and', 'letting',
                                'them', 'linger', '.'],
                     "label": "neg"}

        assert len(instances) == 3
        fields = instances[0].fields
        assert [t.text for t in fields["tokens"].tokens] == instance1["tokens"]
        assert fields["label"].label == instance1["label"]
        fields = instances[1].fields
        assert [t.text for t in fields["tokens"].tokens] == instance2["tokens"]
        assert fields["label"].label == instance2["label"]
        fields = instances[2].fields
        assert [t.text for t in fields["tokens"].tokens] == instance3["tokens"]
        assert fields["label"].label == instance3["label"]

    def test_read_from_file_and_truncates_properly(self):

        reader = SemiSupervisedTextClassificationJsonReader(sequence_length=5)
        ag_path = self.FIXTURES_ROOT / "imdb" / "train.jsonl"
        instances = reader.read(ag_path)
        instances = ensure_list(instances)

        instance1 = {"tokens": ['...', 'And', 'I', 'never', 'thought'],
                     "label": "neg"}
        instance2 = {"tokens": ['The', 'fight', 'scenes', 'were', 'great'],
                     "label": "pos"}
        instance3 = {"tokens": ['The', 'only', 'way', 'this', 'is'],
                     "label": "neg"}

        assert len(instances) == 3
        fields = instances[0].fields
        assert [t.text for t in fields["tokens"].tokens] == instance1["tokens"]
        assert fields["label"].label == instance1["label"]
        fields = instances[1].fields
        assert [t.text for t in fields["tokens"].tokens] == instance2["tokens"]
        assert fields["label"].label == instance2["label"]
        fields = instances[2].fields
        assert [t.text for t in fields["tokens"].tokens] == instance3["tokens"]
        assert fields["label"].label == instance3["label"]
    
    def test_metadata_is_correct(self):

        
        imdb_labeled_path = self.FIXTURES_ROOT / "imdb" / "train.jsonl"
        imdb_unlabeled_path = self.FIXTURES_ROOT / "imdb" / "unlabeled.jsonl"
        reader = SemiSupervisedTextClassificationJsonReader(unlabeled_data_path=imdb_unlabeled_path,
                                                            sequence_length=5)

        instances = reader.read(imdb_labeled_path)
        instances = ensure_list(instances)

        fields = [i.fields for i in instances]

        is_labeled = [f['metadata']['is_labeled'] for f in fields]

        assert is_labeled == [True, True, True, False, False, False]


    def test_samples_properly(self):
        reader = SemiSupervisedTextClassificationJsonReader(sample=1, sequence_length=5)
        ag_path = self.FIXTURES_ROOT / "imdb" / "train.jsonl"
        params = Params({"random_seed": 5, "numpy_seed": 5, "pytorch_seed": 5})
        prepare_environment(params)
        instances = reader.read(ag_path)
        instances = ensure_list(instances)
        instance = {"tokens": ['The', 'fight', 'scenes', 'were', 'great'],
                    "label": "pos"}
        assert len(instances) == 1
        fields = instances[0].fields
        assert [t.text for t in fields["tokens"].tokens] == instance["tokens"]
        assert fields["label"].label == instance["label"]

    def test_samples_according_seed_properly(self):

        reader1 = SemiSupervisedTextClassificationJsonReader(sample=2, sequence_length=5)
        reader2 = SemiSupervisedTextClassificationJsonReader(sample=2, sequence_length=5)
        reader3 = SemiSupervisedTextClassificationJsonReader(sample=2, sequence_length=5)

        imdb_path = self.FIXTURES_ROOT / "imdb" / "train.jsonl"
        params = Params({"random_seed": 5, "numpy_seed": 5, "pytorch_seed": 5})
        prepare_environment(params)
        instances1 = reader1.read(imdb_path)
        params = Params({"random_seed": 2, "numpy_seed": 2, "pytorch_seed": 2})
        prepare_environment(params)
        instances2 = reader2.read(imdb_path)
        params = Params({"random_seed": 5, "numpy_seed": 5, "pytorch_seed": 5})
        prepare_environment(params)
        instances3 = reader3.read(imdb_path)
        fields1 = [i.fields for i in instances1]
        fields2 = [i.fields for i in instances2]
        fields3 = [i.fields for i in instances3]
        tokens1 = [f['tokens'].tokens for f in fields1]
        tokens2 = [f['tokens'].tokens for f in fields2]
        tokens3 = [f['tokens'].tokens for f in fields3]
        text1 = [[t.text for t in doc] for doc in tokens1]
        text2 = [[t.text for t in doc] for doc in tokens2]
        text3 = [[t.text for t in doc] for doc in tokens3]
        assert text1 != text2
        assert text1 == text3

    def filters_properly(self):
        params = Params.from_file(self.FIXTURES_ROOT / 'nvdm' / 'experiment.json')
        reader = SemiSupervisedTextClassificationJsonReader(**params['dataset_reader'])
        instances = reader.read(params['validation_data_path'])
        fields = [i.fields for i in instances]
        tokens = [f['tokens'].tokens for f in fields]
        text = [[t.text for t in doc] for doc in tokens]

        def check_punc(token):
            if token in ('@@PADDING@@', '@@UNKNOWN@@'):
                return False
            puncs = list(string.punctuation)
            puncs.remove('-')
            return bool(set(token).intersection(set(puncs)))

        for doc in text:
            # make sure all tokens len > 3
            assert (np.array([len(token) for token in doc]) > 3).all()
            # make sure no digits in text
            assert (np.array([bool(re.search(r'\d', token)) for token in doc]) is False).all()
            # make sure no punctuation in text
            assert (np.array([check_punc(token) for token in doc]) is False).all()
