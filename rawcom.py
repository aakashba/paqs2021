import pickle

databox = "../qadatasetKstudy"

source = pickle.load(open(databox+"/qatypeA.pkl","rb"))
raw = pickle.load(open(databox +"/context.pkl","rb"))
splitfile = "/nfs/projects/funcom/data/java/output/trainvaltest_ids.pkl"
spliter = pickle.load(open(splitfile,"rb"))

mainfile = dict((fid, raw[fid]) for fid in source) # first filter out the good fids 

raw.clear()

trainfid = spliter['trainfid']

valfid = spliter['valfid']

testfid = spliter['testfid']

ftrain = open(databox+"/output/context.train", 'w')
fval = open(databox+"/output/context.val", 'w')
ftest =open(databox+"/output/context.test", 'w')

train = dict((fid, mainfile[fid]) for fid in trainfid if fid in mainfile.keys()) # split train-val-test

val = dict((fid, mainfile[fid]) for fid in valfid if fid in mainfile.keys())

test = dict((fid, mainfile[fid]) for fid in testfid if fid in mainfile.keys())

mainfile.clear()

for f in train:
    ftrain.write('{}, <s> {} </s>\n'.format(f, train[f]))

for f in val:
    fval.write('{}, <s> {} </s>\n'.format(f, val[f]))

for f in  test:
    ftest.write('{}, <s> {} </s>\n'.format(f, test[f]))


ftrain.close()
fval.close()
ftest.close()

