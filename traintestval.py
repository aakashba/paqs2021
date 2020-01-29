import pickle


splitfile = "../trainvaltest_ids.pkl"
databox = "../qadatasetAstudy"

mainfile = pickle.load(open(databox + "/qatypeA.pkl","rb"))


spliter = pickle.load(open(splitfile,"rb"))

trainfid = spliter['trainfid']

valfid = spliter['valfid']

testfid = spliter['testfid']

train = dict((fid, mainfile[fid]) for fid in trainfid if fid in mainfile.keys())
pickle.dump(train,open(databox + "/train.pkl","wb"))

val = dict((fid, mainfile[fid]) for fid in valfid if fid in mainfile.keys()) 
pickle.dump(val,open(databox + "/val.pkl","wb"))

test = dict((fid, mainfile[fid]) for fid in testfid if fid in mainfile.keys()) 
pickle.dump(test,open(databox + "/test.pkl","wb"))

