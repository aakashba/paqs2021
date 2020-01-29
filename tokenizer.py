import collections
from keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np
# 0 is reserved
# make UNK token something
# make vocab size a requirement on creation
class Tokenizer(object):
    def __init__(self):
        self.word_count = collections.Counter()
        self.w2i = {}
        self.i2w = {}
        self.oov_index = None
        self.vocab_size = None
        self.vectors = {}

    def save(self, path):
        pickle.dump(self, open(path, 'wb'))

    def load(self, path):
        return pickle.load(open(path, 'rb'))

    def train(self, texts, vocab_size):

        if len(self.word_count) != 0:
            raise Exception("To update existing tokenizer with new vocabulary, run update() or update_from_file()")

        
        # takes a list of strings that are space delimited into tokens
        for sent in texts:
            for w in sent.split():
                self.word_count[w] += 1

        self.vocab_size = vocab_size

        # Easily changed but vocab size is essentially defining your max index
        # 0 is reserved and UNK is reserved so you will get vocab_size-2 to get
        # indices from 0-(vocab_size-1) i.e. vocab_size = 50, we get indices 0-49
        for count, w in enumerate(self.word_count.most_common(self.vocab_size-2)):
            self.w2i[w[0]] = count+1
            self.i2w[count+1] = w[0]
        self.oov_index = min([self.vocab_size-1, len(self.word_count)+1])
        self.vocab_size = self.oov_index+1
        self.w2i['<UNK>'] = self.oov_index
        self.w2i['<NULL>'] = 0
        self.i2w[0] = '<NULL>'
        self.i2w[self.oov_index] = '<UNK>'

    def train_from_file(self, path, vocab_size,typ):
        if len(self.word_count) != 0:
            raise Exception("To update existing tokenizer with new vocabulary, run update() or update_from_file()")

        # This is for our file representation of "fid, text\n"
        self.vocab_size = vocab_size

        for line in open(path):
            if typ == 0:
                tmp = [x.strip() for x in line.split(',',1)]
            # takes a list of strings that are space delimited into tokens
                fid = tmp[0]
                sent = tmp[1]
            elif typ == 1:
                tmp = [x.strip() for x in line.split(',',2)]
                fid = tmp[0]
                sent = tmp[2]
            for w in sent.split():
                self.word_count[w] += 1

        # Easily changed but vocab size is essentially defining your max index
        # 0 is reserved and UNK is reserved so you will get vocab_size-2 to get
        # indices from 0-(vocab_size-1) i.e. vocab_size = 50, we get indices 0-49
        for count, w in enumerate(self.word_count.most_common(self.vocab_size-2)):
            self.w2i[w[0]] = count+1
            self.i2w[count+1] = w[0]
        self.oov_index = min([self.vocab_size-1, len(self.word_count)+1])
        self.vocab_size = self.oov_index+1
        self.w2i['<UNK>'] = self.oov_index
        self.w2i['<NULL>'] = 0
        self.i2w[0] = '<NULL>'
        self.i2w[self.oov_index] = '<UNK>'
    
    def update(self, texts):
        # takes a list of strings that are space delimited into tokens
        for sent in texts:
            for w in sent.split():
                self.word_count[w] += 1

        # reset w2i and i2w for new vocab
        self.w2i = {}
        self.i2w = {}

        # Easily changed but vocab size is essentially defining your max index
        # 0 is reserved and UNK is reserved so you will get vocab_size-2 to get
        # indices from 0-(vocab_size-1) i.e. vocab_size = 50, we get indices 0-49
        for count, w in enumerate(self.word_count.most_common(self.vocab_size-2)):
            self.w2i[w[0]] = count+1
            self.i2w[count+1] = w[0]
        self.oov_index = min([self.vocab_size-1, len(self.word_count)+1])
        self.vocab_size = self.oov_index+1
        self.w2i['<UNK>'] = self.oov_index
        self.w2i['<NULL>'] = 0
        self.i2w[0] = '<NULL>'
        self.i2w[self.oov_index] = '<UNK>'      

    def update_from_file(self, path, typ):
        # takes a list of strings that are space delimited into tokens
        for line in open(path):
            if typ == 0:
                tmp = [x.strip() for x in line.split(',',1)]
                fid = tmp[0]
                sent = tmp[1]
            elif typ == 1:
                tmp = [x.strip() for x in line.split(',',2)]
                fid = tmp[0]
                sent = tmp[2]
            for w in sent.split():
                self.word_count[w] += 1

        # reset w2i and i2w for new vocab
        self.w2i = {}
        self.i2w = {}
        
        # Easily changed but vocab size is essentially defining your max index
        # 0 is reserved and UNK is reserved so you will get vocab_size-2 to get
        # indices from 0-(vocab_size-1) i.e. vocab_size = 50, we get indices 0-49
        for count, w in enumerate(self.word_count.most_common(self.vocab_size-2)):
            self.w2i[w[0]] = count+1
            self.i2w[count+1] = w[0]
        self.oov_index = min([self.vocab_size-1, len(self.word_count)+1])
        self.vocab_size = self.oov_index+1
        self.w2i['<UNK>'] = self.oov_index
        self.w2i['<NULL>'] = 0
        self.i2w[0] = '<NULL>'
        self.i2w[self.oov_index] = '<UNK>'

    def set_vocab_size(self, vocab_size):
        self.vocab_size = vocab_size
        # reset w2i and i2w for new vocab
        self.w2i = {}
        self.i2w = {}
        
        # Easily changed but vocab size is essentially defining your max index
        # 0 is reserved and UNK is reserved so you will get vocab_size-2 to get
        # indices from 0-(vocab_size-1) i.e. vocab_size = 50, we get indices 0-49
        for count, w in enumerate(self.word_count.most_common(self.vocab_size-2)):
            self.w2i[w[0]] = count+1
            self.i2w[count+1] = w[0]
        self.oov_index = min([self.vocab_size-1, len(self.word_count)+1])
        self.w2i['<UNK>'] = self.oov_index
        self.w2i['<NULL>'] = 0
        self.i2w[0] = '<NULL>'
        self.i2w[self.oov_index] = '<UNK>'



    def texts_to_sequences(self, texts, typ,  maxlen=None, padding='post', truncating='post', value=0):

        if len(self.word_count) == 0:
            raise Exception("Tokenizer has not been trained, no words in vocabulary.")

        all_seq = list()
        for sent in texts:
            seq = []
            for w in sent.split():
                try:
                    seq.append(self.w2i[w])
                except:
                    seq.append(self.oov_index)

                if maxlen is not None:
                    if len(seq) == maxlen:
                        break

            all_seq.append(seq)
            
        return pad_sequences(all_seq, maxlen=maxlen, padding=padding, truncating=truncating, value=value)

    def texts_to_sequences_from_file(self, path, typ, maxlen=50, padding='post', truncating='post'):

        if len(self.word_count) == 0:
            raise Exception("Tokenizer has not been trained, no words in vocabulary.")

        all_seq = {}
        if typ == 0:
            for line in open(path):
                seq = []
                tmp = [x.strip() for x in line.split(',',1)]
                fid = tmp[0]
                sent = tmp[1]
                for w in sent.split():
                    try:
                        seq.append(self.w2i[w])
                    except:
                        seq.append(self.oov_index)

                    if maxlen is not None:
                        if len(seq) == maxlen:
                            break
                all_seq[fid] = seq
            return {key: newval for key, newval in zip(all_seq.keys(), pad_sequences(all_seq.values(), maxlen=maxlen, padding=padding, truncating=truncating, value=0))}
        
        elif typ == 1:
            for line in open(path):
                seq = []
                tmp = [x.strip() for x in line.split(',',2)]
                fid = tmp[0]
                sid = tmp[1]
                sent = tmp[2]
                for w in sent.split():
                    try:
                        seq.append(self.w2i[w])
                    except:
                        seq.append(self.oov_index)

                    if maxlen is not None:
                        if len(seq) == maxlen:
                            break
                if fid not in all_seq.keys():        
                    all_seq[fid] = {}

                all_seq[fid][sid]= seq
                finaldict={}
            for f in all_seq.keys():
                finaldict.update({f:{skey: newval for skey, newval in zip(all_seq[f].keys(), pad_sequences(all_seq[f].values(), maxlen=maxlen, padding=padding, truncating=truncating, value=0))}})
            return finaldict

    def seq_to_text(self, seq):
        return [self.i2w[x] for x in seq]

    def forw2v(self, seq):
        return [self.i2w[x] for x in seq if self.i2w[x] not in ['<NULL>', '<s>', '</s>']]
