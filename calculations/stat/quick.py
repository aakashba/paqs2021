import pickle

x = pickle.load(open("RQ2stats.pkl","rb"))

calcs = {}

for query in x['correct']:
    calcs.update({query:{'none':0,'rel':0,'acc':0}})
    for i in range(len(x['correct'][query])):
        if x['correct'][query][i] == 0:
            if x['relevant'][query][i] ==0 and x['accurate'][query][i] ==0:
                calcs[query]['none'] += 1
            elif x['relevant'][query][i] ==1 and x['accurate'][query][i] ==0:
                calcs[query]['rel'] += 1
            elif x['relevant'][query][i] ==0 and x['accurate'][query][i] ==1:
                calcs[query]['acc'] += 1



for query in calcs:
    print(query)
    for stat in calcs[query]:
        print(stat)
        print(calcs[query][stat]/sum(list(calcs[query].values())))





