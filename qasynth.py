# Programmer Assisted Question-answer Sytenthesis (PAQS)

from bs4 import BeautifulSoup
from html.parser import HTMLParser
from myutils import prep, drop, print_ast
import multiprocessing
import pickle
import re
from sys import argv
import nltk
import os
import statistics
import numpy as np
import random
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import inflect

# pickle with question layout paraphrases as a dictionary
Questions = pickle.load(open("questions.pkl","rb"))

# Answer layouts
Q1 = Questions['Q1']
A1 = "the return type for this method is "
Q2 = Questions['Q2'] 
A2 = "the arguments taken by this method are "
Q3 = Questions['Q3']
A3 = "I found method definition: <funcode>  "
Q4 = Questions['Q4']
A4 = " I found func that takes arg_list and returns f_ret "
Q5 = Questions['Q5']
A5 = " The signature for this method : "
Q6 = Questions['Q6']
A6 = " This method does_this "
Q7 = Questions['Q7']
A7 = "I found func that does_this "
Q8 = Questions['Q8']
#A8P = "Yes"



qid = 0
aid = 0

# filtered list of comments/fid
comfile = pickle.load(open("goodcoms.pkl","rb"))


ncount = 0

def comqa(idf,com,fname,fname2):
    nonaction = "am are is be was were has been had"
    p = inflect.engine()
    qa = dict()
    qa2 = dict()
    com = "Paris "+com  # random noun introduced as tagged does not handle sentences starting with nouns well
    comsplit = com.split()
    tags = nltk.pos_tag(nltk.word_tokenize(com))
    start = -2
    cpos = 0
    end = len(comsplit)
    if 'return' in comsplit[1] or 'get' in comsplit[1] or 'set' in comsplit[1] or 'give' in comsplit[1]:
        start = 1
    elif 'getter' in comsplit[1] and 'for' in comsplit[2]:
        comsplit[1] = "get"
        del comsplit[2]
    elif 'setter' in comsplit[1] and 'for' in comsplit[2]:
        comsplit[1] = "set"
        del comsplit[2]
    else:
        for x in tags:
            if "VB" in x[1] and start == -2:
                if 'is' ==  x[0] or x[0] in nonaction:   # filters out instances of paris verb etc..
                    start = -2
                else:
                    start = cpos
            cpos +=1
    if start == 0 or start == -2:
        raise Exception('noverb')
    
    action = comsplit[start:end]
    verb = list(action[0])
    if 's' in verb[-1]:  # creating the "Do_this" tense of actions
        if 'e' in verb[-2]:
            action[0] = WordNetLemmatizer().lemmatize(action[0],'v') 
        elif 'i' in verb[-2]:
            raise Exception('noverb') 
        else:
            action[0] = WordNetLemmatizer().lemmatize(action[0],'v')
        dothis = " ".join(action)
    else:
        action[0] = WordNetLemmatizer().lemmatize(action[0],'v')
        dothis = " ".join(action)

    doesthis = makedoesthis(dothis)

    qa.update({"Q"+str(qID()):random.choice(Q6).lower()})
    qa.update({"A"+str(aID()):A6.replace('does_this',doesthis).lower()})
    qa2.update({"Q"+str(qID()):random.choice(Q7).replace('do_this',dothis).replace('does_this',doesthis).lower()})
    qa2.update({"A"+str(aID()):replace(A7,{'func':fname, 'does_this':doesthis}).lower()})
    qa.update({"Q"+str(qID()):random.choice(Q8).replace('func',fname).replace('do_this',dothis).replace('does_this',doesthis).lower()})
    qa.update({"A"+str(aID()):"Yes it does".lower()})
    qa.update({"Q"+str(qID()):random.choice(Q8).replace('func',fname2).replace('do_this',dothis).replace('does_this',doesthis).lower()})
    qa.update({"A"+str(aID()):"No it does not".lower()})

    return qa,qa2


# method to convert do_this type of actions into does_this tense
def makedoesthis(act):
    p = inflect.engine()
    actsplit = act.split()
    if "this" == actsplit[0] or "is" == actsplit[0]:
        return act
    else:
        actsplit[0] = p.plural(actsplit[0])
        pact = " ".join(actsplit)
        return pact

def replace(string, substitutions):

    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)

def qID():
    global qid
    qid +=1
    return qid
def aID():
    global aid
    aid +=1
    return aid

datasetloc = 'srcmldat'

# loading srcml to aid finding the elements in code
prep('loading srcmlunits... ')
srcmlunits = pickle.load(open(datasetloc + '/srcml-standard.pkl', 'rb'))
sml2 = pickle.load(open(datasetloc + '/srcml-final-allcoms.pkl', 'rb'))

for key, val in sml2.items():
    srcmlunits[key] = val

drop()

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.parentstack = list()
        self.qasynth = dict()
        self.qasynth2 = dict()
        self.dataseq = list()
        self.context = list()
        self.tagseq = list()
        self.pstart = 0
        self.pend = 0
        self.lasttexttag = -1
        self.curtag = -1
        self.tagidx = -1
        self.ptype = 0
        self.dtype = 0
        self.ret = "null"
        self.func ="0blank0"
        
    def handle_starttag(self, tag, attrs):
        self.parentstack.append(self.curtag)
        self.tagidx += 1
        self.dtype = 0
        if tag == "name":
            if self.tagseq[-1] == "type" and self.tagseq[-2] == "specifier":
                self.dtype = 1
            elif self.tagseq[-1] == "specifier" and self.tagseq[-2] == "constructor":
                self.dtype = 1

        if tag == "parameter_list" and self.ptype == 0:
            self.ptype = 2

        self.tagseq.append(tag)
        self.curtag = self.tagidx
        
    def handle_endtag(self, tag):
        self.curtag = self.parentstack.pop()
        
    
    def handle_data(self, data):
        if(data != ''):
            for d in data.split(' '):
                self.context.append(d)
                if d != '' and '\n' not in d and '\t' not in d:
                    self.parentstack.append(self.curtag)
                    self.tagidx +=1

                    if self.dtype == 1:
                        self.ret = d
                    if len(self.dataseq) >=1:

                        if self.dataseq[-1] == self.ret and self.func is "0blank0":
                            self.func = d

                        if self.ptype == 2 and "(" in d and self.pstart == 0:
                            self.pstart = self.dataseq.index(self.dataseq[-1])+ 1

                        if ")" in d and self.pend == 0:
                            self.pend = self.dataseq.index(self.dataseq[-1])+ 2

                    self.lasttexttag = self.tagidx
                    self.dataseq.append(d)
                    self.curtag = self.tagidx
                    self.curtag = self.parentstack.pop()
        
    def get_qa(self):
        if self.func != "0blank0" and "(" not in self.func :  # filter out bad no return defined functions
            self.paralist = self.dataseq[self.pstart:self.pend]
            self.fsig = self.dataseq[ : self.pend]
            self.fdef = self.dataseq[ : -1]
            self.qasynth.update({"Q"+str(qID()):  random.choice(Q1).lower()})
            self.qasynth.update({"A"+str(aID()):  (A1 + self.ret).lower()})
            self.qasynth.update({"Q"+str(qID()):  random.choice(Q2).lower()})
            if len(self.paralist) < 3 :
                self.qasynth.update({"A"+str(aID()): " this method takes no arguments to the function"})
            else:
                self.qasynth.update({"A"+str(aID()):  (A2 + " ".join(self.paralist).lower()})

            self.qasynth.update({"Q"+str(qID()):  random.choice(Q3).replace('func',self.func).lower()})
            self.qasynth.update({"A"+str(aID()):  A3.lower() })

            if len(self.paralist) > 3 :
                modparalist = [x for x in self.paralist if ',' not in x ] # remove commas for consistent extraction of parameters
                for i in modparalist[1:-1:2]:
                    self.qasynth2.update({"Q"+str(qID()): replace(random.choice(Q4),{"f_arg":i, "f_ret":self.ret}).lower()})
                    self.qasynth2.update({"A"+str(aID()): replace(A4,{"func":self.func , "arg_list": " ".join(self.paralist) , "f_ret":self.ret }).lower()})

            self.qasynth.update({"Q"+str(qID()):  random.choice(Q5).lower()})
            self.qasynth.update({"A"+str(aID()):  A5 + " ".join(map(str, self.fsig)).lower()})
            context = " ".join(self.context)
            context = replace(context,{"\n":" nl", "\t":" t "})
            return self.qasynth, self.qasynth2 , " ".join(map(str,self.fsig)).lower(), self.func.lower() , context.lower()
        else:
            raise Exception("blank")

c = 0

def xmldecode(unit):
    parser = MyHTMLParser()
    parser.feed(unit)
    return(parser.get_qa())

qadict = dict()
qadict2 = dict()
b = 0
badcoms = list()
prep('parsing xml... ')
projcontext = dict()
fnames = dict()
projcontextfid = dict()
fcontext = dict()
fnamelist= list()


for pid,value in comfile.items(): 
    for fid,comment in value.items():
        print(fid)
        try:
            unit = srcmlunits[fid]
            qaset, qaset2, sig, fname, context = xmldecode(unit)

        except:

            badcoms.append(fid)
            c+= 1
            continue

        fnamelist.append(fname)

        projform =comment.replace('\n',' nl ') + sig + ' nl '

        if pid in projcontext.keys():
            fnames[pid].update({fid:fname})
            projcontext[pid] += projform
        else:
            felem = {fid:fname}
            fnames.update({pid:felem})
            projcontext.update({pid:projform})

        contcom = comment.replace('\n',' nl ') + context
        fcontext.update({fid:contcom})
        qadict.update({fid:qaset})
        qadict2.update({fid:qaset2})
    break
# loops again to be able to create the negative cases as well for the yes/no question type
for pid,value in comfile.items(): 
    for fid,comment in value.items():
        print(fid)
        if fid in qadict.keys():
            try:
                funcname = fnames[pid][fid]
                qa,qa2 = comqa(fid, comment,funcname,random.choice([x for y,x in fnames[pid].items() if x != funcname]))
                qadict[fid].update(qa)
                qadict2[fid].update(qa2)
                projcontextfid.update({fid:pid})  # each fid directs to its pid 
            except:
                badcoms.append(fid)
                c += 1
                del fcontext[fid]
                del qadict[fid]
                del qadict2[fid]# remove the fids that give exception for the comment function.
    break        
    
drop()

print('bad:',c )
prep('writing pkl... ')
bid = open("badfids.pkl","wb")
pickle.dump(badcoms,bid)
bid.close()
fcontfile = open("/nfs/projects/paqs/qadatasetKstudy/context.pkl","wb")
pickle.dump(fcontext, fcontfile)
fcontfile.close()
projcontfile = open("/nfs/projects/paqs/qadatasetUstudy/pcontext.pkl","wb")
pickle.dump(projcontext,projcontfile)  #context per project only
projcontfile.close()
contfile = open("/nfs/projects/paqs/qadatasetUstudy/context.pkl","wb")
pickle.dump(projcontextfid,contfile) # list of fids with their pids
contfile.close()
qafile = open("/nfs/projects/paqs/qadatasetKstudy/qatypeA.pkl","wb") 
pickle.dump(qadict,qafile)
qafile.close()
qa2file = open("/nfs/projects/paqs/qadatasetUstudy/qatypeB.pkl","wb") 
pickle.dump(qadict2,qa2file)
qa2file.close()
print("Number of unique fnames " , len(fnamelist))
prep('cleaning up... ')

drop()

