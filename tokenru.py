from tokenizer import Tokenizer
import sys

#ques_vocab = 10000
ans_vocab = 20000
con_vocab = 100000
databox='../qadatasetKstudy'

quesans= databox + '/quesans.cont'
ques_file = databox + '/output/questions.tok'
ans_file = databox + '/output/answers.tok'

confile = databox + '/context.cont' #context use a different tokenizer as they have only fid but questions have qid and answers have aid. change in tokenizer.py
con_file = databox + '/output/context.tok'

q = Tokenizer()
q.train_from_file(quesans, ans_vocab,1)
q.save(ques_file)
q.save(ans_file)

c = Tokenizer()
c.train_from_file(confile, con_vocab,0)
c.save(con_file)
