import torch
from torch.autograd import Variable
'''
This code is adapted from https://github.com/salesforce/awd-lstm-lm/
'''

def repackage_hidden(h):
    """Wraps hidden states in new Variables, to detach them from their history."""
    if type(h) == Variable:
        return Variable(h.data)
    else:
        return tuple(repackage_hidden(v) for v in h)

def batchify(data, bsz, args):
    # Work out how cleanly we can divide the dataset into bsz parts.
    nbatch = data.size(0) // bsz
    # Trim off any extra elements that wouldn't cleanly fit (remainders).
    data = data.narrow(0, 0, nbatch * bsz)
    # Evenly divide the data across the bsz batches.
    data = data.view(bsz, -1).t().contiguous()
    if args.cuda:
        data = data.cuda()
    return data

def get_batch(source, i, args, seq_len=None, evaluation=False):
    seq_len = min(seq_len if seq_len else args.bptt, len(source) - 1 - i)
    data = Variable(source[i:i+seq_len], volatile=evaluation)
    target = Variable(source[i+1:i+1+seq_len].view(-1))
    return data, target

def model_save(fn, model, criterion, optimizer, epoch):
    with open(fn, 'wb') as f:
        torch.save([model, criterion, optimizer, epoch], f)

def model_load(fn):
    with open(fn, 'rb') as f:
        model, criterion, optimizer, epoch = torch.load(f)
        return model, criterion, optimizer, epoch
