import pickle
from collections import OrderedDict
import os
from statistics import mean
import copy

datbox = "/nfs/projects/paqs/userstudy/data/pkl/ftagged/interactions/"
statsum = {'relevant':0,'accurate':0,'correct':0,'numtillcor':0,'complete':0,'concise':0}
queries = ['Query1','Query2','Query3','Query4','Query5','Query6']
rating = {'sa':1,'a':2,'u':3,'d':4,'sd':5}
statlen = copy.deepcopy(statsum)
firstfive = copy.deepcopy(statsum)
firstlen = copy.deepcopy(statsum)
afterfive = copy.deepcopy(statsum)
afterlen = copy.deepcopy(statsum)
neutralsum = copy.deepcopy(statsum)
neutrallen = copy.deepcopy(statsum)
stats = {'relevant':{},'accurate':{},'correct':{},'numtillcor':{},'complete':{},'concise':{}}
finalstat = copy.deepcopy(stats)
statsRQ2 = copy.deepcopy(stats)
statderived = copy.deepcopy(stats)
for quality in finalstat:
    finalstat[quality].update({'Overall':0,'Neutral':0,'firstfive':0,'afterfive':0})
for sub in os.listdir(datbox):
    subject = sub.split('.')[0]
    count = 0
    for quality in stats.keys():
        stats[quality].update({subject:OrderedDict()})
        statsRQ2[quality].update({subject:OrderedDict()})
        stats[quality][subject].update({'neutral':[]})
        statderived[quality].update({subject:OrderedDict()})
    datfile = pickle.load(open(datbox+sub,'rb'))
    for fid in datfile:
        count += 1
        for quality in stats.keys():
            stats[quality][subject].update({fid:[]})
            statsRQ2[quality][subject].update({fid:{'Query1':[],'Query2':[],'Query3':[],'Query4':[],'Query5':[],'Query6':[]}})
            statderived[quality][subject].update({fid:0})
        for reading in datfile[fid]:
            for query in queries:
                if query in reading.keys():
                    rel = rating[reading['r1']]
                    stats['relevant'][subject][fid].append(rel)
                    statsRQ2['relevant'][subject][fid][query].append(rel)

                    acc = rating[reading['r2']]
                    stats['accurate'][subject][fid].append(acc)
                    statsRQ2['accurate'][subject][fid][query].append(acc)

                    if 'a' in reading['r2'] and 'a' in reading['r1']:
                        num = 0
                        if len(stats['correct'][subject][fid]) >= 1:
                            cor = stats['correct'][subject][fid]
                            cor.reverse()
                            for x in cor:
                                if x == 0:
                                    num +=1
                                else:
                                    break
                        stats['numtillcor'][subject][fid].append(num)
                        statsRQ2['numtillcor'][subject][fid][query].append(num)
                        statsRQ2['correct'][subject][fid][query].append(1)
                        stats['correct'][subject][fid].append(1)
                    else:
                        statsRQ2['correct'][subject][fid][query].append(0)
                        stats['correct'][subject][fid].append(0)
            

                    comp = rating[reading['r3']]
                    stats['complete'][subject][fid].append(comp)
                    statsRQ2['complete'][subject][fid][query].append(comp)

                    conc = rating[reading['r4']]
                    stats['concise'][subject][fid].append(conc)
                    statsRQ2['concise'][subject][fid][query].append(conc)

                    if 'u' in reading['r1']:
                        stats['relevant'][subject]['neutral'].append(1)
                    else:
                        stats['relevant'][subject]['neutral'].append(0)

                    if 'u' in reading['r2']:
                        stats['accurate'][subject]['neutral'].append(1)
                    else:
                        stats['accurate'][subject]['neutral'].append(0)

                    if 'u' in reading['r3']:
                        stats['complete'][subject]['neutral'].append(1)
                    else:
                        stats['complete'][subject]['neutral'].append(0)

                    if 'u' in reading['r4']:
                        stats['concise'][subject]['neutral'].append(1)
                    else:
                        stats['concise'][subject]['neutral'].append(0)
        for quality in stats.keys():
            if quality == 'numtillcor' and stats[quality][subject][fid] == []:  #numtillcorr doesnt work if all=incorrect, only happens when UNK is assumed inaccurate
                statderived[quality][subject][fid] = 'NULL'
            else:
                statderived[quality][subject][fid] = mean(stats[quality][subject][fid])
                ssum = sum(stats[quality][subject][fid])
                slen = len(stats[quality][subject][fid])
                statsum[quality] += ssum
                statlen[quality] += slen
                print('count',count)
                print('fid',fid)
                if count <= 5:
                    print('subject',subject)
                    print('tillfive')
                    firstfive[quality] += ssum
                    firstlen[quality] += slen
                else:
                    print('subject',subject)
                    print('afterfive')
                    afterfive[quality] += ssum
                    afterlen[quality] += slen

    for quality in stats.keys():
        neutralsum[quality] += sum(stats[quality][subject]['neutral'])
        neutrallen[quality] += len(stats[quality][subject]['neutral'])


statsRQ2mean = copy.deepcopy(statsRQ2)

for quality in finalstat.keys():
    finalstat[quality]['firstfive'] = firstfive[quality]/firstlen[quality]
    finalstat[quality]['afterfive'] = afterfive[quality]/afterlen[quality]
    finalstat[quality]['Overall'] = statsum[quality]/statlen[quality]
    if neutrallen[quality] == 0:     #for numtillcor and correct
        finalstat[quality]['Neutral'] = 'N/A'
    else:
        finalstat[quality]['Neutral'] = neutralsum[quality]/neutrallen[quality]
#    for query in queries:
 #       statsRQ2mean[quality][query]= mean(statsRQ2[quality][query])
    
statfile = open("statraw/stats.pkl","wb")
derivedfile = open("statraw/StatDerived.pkl","wb")
RQ2file = open("statraw/RQ2stats.pkl","wb")
RQ2mean = open("statraw/RQ2mean.pkl","wb")
finalfile = open("statraw/finalstats.pkl","wb")
pickle.dump(statsRQ2,RQ2file)
pickle.dump(stats,statfile)
pickle.dump(statderived,derivedfile)
pickle.dump(statsRQ2mean,RQ2mean)
pickle.dump(finalstat,finalfile) 
statfile.close()
finalfile.close()
RQ2file.close()
RQ2mean.close()
derivedfile.close()




            
                






            

