import pickle
databox = "/nfs/projects/paqs/qadatasetAstudy"

source = pickle.load(open(databox + "/val.pkl","rb"))

questions = databox + "/output/ques.val"
answers = databox + "/output/ans.val"

fqes = open(questions, 'w')
fans = open(answers, 'w')

for fid, value in source.items():
    for sid, sentence in value.items():
        if "Q" in sid:
            fqes.write('{},{}, <s> {} </s>\n'.format(fid, sid, sentence))
        elif "A" in sid:
            fans.write('{},{}, <s> {} </s>\n'.format(fid, sid, sentence))

fqes.close()
fans.close()

