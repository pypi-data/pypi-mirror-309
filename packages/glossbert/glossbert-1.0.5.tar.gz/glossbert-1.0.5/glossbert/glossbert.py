# Python package for Word Sentence Disambiguation (WSD) using GlossBERT model.
# Copyright (c) 2024 José María Cruz Lorite
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import torch
from torch.nn.functional  import softmax
from transformers import AutoTokenizer, BertForSequenceClassification

import nltk
from nltk.corpus import wordnet as wn

# set up logging
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt = '%m/%d/%Y %H:%M:%S',
    level = logging.INFO
)


class GlossBERT:
    """GlossBERT model wrapper class for Word Sense Disambiguation (WSD)"""
    
    LABELS = ["0", "1"]
    """The label list for the GlossBERT model"""
    
    def __init__(self, model="kanishka/GlossBERT", cuda=True):
        """Initialize GlossBERT model
        
        Args:
            model (str): model name, default is "kanishka/GlossBERT"
            cuda (bool): whether to use CUDA, default is True
        """
        logger.info("Initializing GlossBERT model...")
        self.device = torch.device("cuda" if torch.cuda.is_available() and cuda else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model, do_lower_case=True)
        self.model = BertForSequenceClassification.from_pretrained(model, num_labels=len(self.LABELS))
        self.model.to(self.device)
        logger.info("GlossBERT model initialized.")
        
        # download WordNet data
        logger.info("Loading WordNet data...")
        nltk.download('wordnet')
        wn.ensure_loaded()
        logger.info("WordNet data loaded.")
    
    def _truncate_seq_pair(self, tokens_a, tokens_b, max_length):
        """Truncates a sequence pair in place to the maximum length.
        
        Args:
            tokens_a (List[str]): tokens of the first sequence
            tokens_b (List[str]): tokens of the second sequence
            max_length (int): maximum sequence length
        """
        # This is a simple heuristic which will always truncate the longer sequence
        # one token at a time. This makes more sense than truncating an equal percent
        # of tokens from each, since if one sequence is very short then each token
        # that's truncated likely contains more information than a longer sequence.
        while True:
            total_length = len(tokens_a) + len(tokens_b)
            if total_length <= max_length:
                break
            if len(tokens_a) > len(tokens_b):
                tokens_a.pop()
            else:
                tokens_b.pop()
    
    def _context_gloss_pairs(self, sentence:str, start: int, end: int, lemma: str, pos:str=None):
        """Construct context gloss pairs for the target word
        
        Args:
            sentence (str): input sentence
            start (int): start index of the target word (inclusive)
            end (int): end index of the target word (exclusive)
            lemma (str): target word lemma
            pos (str): target word part-of-speech tag, default is None
        Returns:
            List[Tuple[str, str, str, str, str, str]]: candidate context gloss pairs
        """
        # check the sentence is not empty
        assert len(sentence) != 0, "sentence is empty"
        
        # check the target word indices are valid
        assert 0 <= start and start < end and end <= len(sentence), "word indices are out of range"
        
        # get synsets of the target word
        if pos is None:
            synsets = wn.synsets(lemma)
        else:
            synsets = wn.synsets(lemma, pos=pos)
        
        # check if there are synsets, otherwise return an empty list
        if len(synsets) == 0:
            return []
        
        target = sentence[start:end]
        try:
            # this will raise an exception if the target word is at the end of the sentence
            _sentence = sentence[:start] + '"' + target + '"' + sentence[end:]
        except:
            _sentence = sentence[:start] + '"' + target + '"'
        
        # construct context gloss pairs
        candidates = []
        for syn in synsets:
            gloss = syn.definition()
            candidates.append((_sentence, f"{target} : {gloss}", syn, target, gloss))
        
        return candidates
    
    def _convert_to_features(self, candidates, max_seq_length=512):
        """Convert context gloss pairs to input features
        
        Args:
            candidates: The input candidates
            max_seq_length (int): maximum sequence length, default is 512
        Returns:
            Tuple: input candidates converted to features
        """
        features = []
        for item in candidates:
            text_a = item[0] # sentence
            text_b = item[1] # gloss
           
            tokens_a = self.tokenizer.tokenize(text_a)
            tokens_b = self.tokenizer.tokenize(text_b)
            self._truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
            tokens = ["[CLS]"] + tokens_a + ["[SEP]"]
            segment_ids = [0] * len(tokens)
            tokens += tokens_b + ["[SEP]"]
            segment_ids += [1] * (len(tokens_b) + 1)
            
            input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
            
            # The mask has 1 for real tokens and 0 for padding tokens. Only real
            # tokens are attended to.
            input_mask = [1] * len(input_ids)
            
            # Zero-pad up to the sequence length.
            padding = [0] * (max_seq_length - len(input_ids))
            input_ids += padding
            input_mask += padding
            segment_ids += padding
            
            assert len(input_ids) == max_seq_length
            assert len(input_mask) == max_seq_length
            assert len(segment_ids) == max_seq_length
            
            features.append({
                "input_ids": input_ids,
                "input_mask": input_mask,
                "segment_ids": segment_ids
            })
        
        return features
    
    def __call__(self, sentence:str, start: int, end: int, lemma: str, pos:str=None):
        """Perform Word Sense Disambiguation (WSD) using GlossBERT model
        
        Args:
            sentence (str): input sentence
            start (int): start index of the target word
            end (int): end index of the target word
            lemma (str): target word lemma
            pos (str): target word part-of-speech tag, default is None
        Returns:
            Tuple[str, str]: sense key and gloss of the target word
        """
        candidates = self._context_gloss_pairs(sentence, start, end, lemma, pos)
        features = self._convert_to_features(candidates)
        
        # convert features to tensors
        input_ids = torch.tensor([f["input_ids"] for f in features], dtype=torch.long)
        input_mask = torch.tensor([f["input_mask"] for f in features], dtype=torch.long)
        segment_ids = torch.tensor([f["segment_ids"] for f in features], dtype=torch.long)
        
        # perform inference
        self.model.eval()
        input_ids = input_ids.to(self.device)
        input_mask = input_mask.to(self.device)
        segment_ids = segment_ids.to(self.device)
        
        with torch.no_grad():
            output = self.model(
                input_ids=input_ids,
                token_type_ids=segment_ids,
                attention_mask=input_mask,
                labels=None
            )
        
        logits_ = softmax(output.logits, dim=-1)
        logits_ = logits_.detach().cpu().numpy()
        
        # order candidates by logits_ and return a list of tuples (score, synset)
        results = [(logits_[i][1], candidates[i][2]) for i in range(len(candidates))]
        results.sort(reverse=True)
        return results
