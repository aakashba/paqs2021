import pickle

databox = "../qadatasetKstudy"

source = pickle.load(open(databox+"/qatypeA.pkl","rb"))
raw = pickle.load(open(databox +"/context.pkl","rb"))

quesans  = open(databox+"/quesans.cont", 'w')
context  = open(databox+"/context.cont", 'w')


for fid,value in source.items() :
    for sid, sentence in value.items():
        quesans.write('{}, {},  <s> {} </s>\n'.format(fid,sid, sentence))

for f in raw:
        context.write('{}, <s> {} </s>\n'.format(f, raw[f]))

quesans.close()
context.close()
