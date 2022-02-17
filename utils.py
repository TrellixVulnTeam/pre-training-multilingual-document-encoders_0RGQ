""" Utility functions to be used while the training."""
import argparse

import torch
from torch import Tensor
from nltk import sent_tokenize


def cos_sim(a: Tensor, b: Tensor):
    """
    Computes the cosine similarity cos_sim(a[i], b[j]) for all i and j.
    :return: Matrix with res[i][j]  = cos_sim(a[i], b[j])

    Taken from https://github.com/UKPLab/sentence-transformers/blob/master/sentence_transformers/util.py
    """
    if not isinstance(a, torch.Tensor):
        a = torch.tensor(a)

    if not isinstance(b, torch.Tensor):
        b = torch.tensor(b)

    if len(a.shape) == 1:
        a = a.unsqueeze(0)

    if len(b.shape) == 1:
        b = b.unsqueeze(0)

    a_norm = torch.nn.functional.normalize(a, p=2, dim=1)
    b_norm = torch.nn.functional.normalize(b, p=2, dim=1)
    return torch.mm(a_norm, b_norm.transpose(0, 1))


def tokenize(example, tokenizer, args: argparse.Namespace):

    def tokenize_helper(article, tokenizer, args: argparse.Namespace):
        sentences = [tokenizer.encode(sentence, add_special_tokens=False) for sentence in sent_tokenize(article)]
        sentences = [sentence[:args.max_seq_length - 2] for sentence in sentences]
        sentences = [[tokenizer.convert_tokens_to_ids("[CLS]")] + sentence + [tokenizer.convert_tokens_to_ids("[SEP]")] for sentence in sentences]

        sentence_lengths = [len(sentence) for sentence in sentences]
        # TODO: check for attention_mask ID
        mask = [[1]*sen_len for sen_len in sentence_lengths]

        return sentences, mask

    # TODO: make article number dynamic
    for i in range(1, 3):
        example[f"article_{i}"], example[f"mask_{i}"] = tokenize_helper(example[f"article_{i}"], tokenizer, args)

    return example
