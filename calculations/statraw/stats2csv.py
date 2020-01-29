import csv
import pickle


finalstat = pickle.load(open("finalstats.pkl","rb"))


with open('finalstat.csv','a') as f:
    w = csv.writer(f)
    w.writerow(['statistics']+list(finalstat['accurate'].keys()))
    for quality in finalstat:
        w.writerow([quality]+list(finalstat[quality].values()))

stats = pickle.load(open("stats.pkl","rb"))

for quality in stats:
    with open(quality+'.csv','a') as s:
        w = csv.writer(s)
        w.writerow(['subject','fid','response'])
        for subject in stats[quality]:
            del stats[quality][subject]['neutral']
            for fid in stats[quality][subject]:
                for resp in stats[quality][subject][fid]:
                    w.writerow([subject,fid,resp])

rq2 = pickle.load(open("RQ2mean.pkl","rb"))

with open('RQ2mean.csv','a') as r:
    w = csv.writer(r)
    w.writerow(['questions']+list(rq2['accurate'].keys()))
    for quality in rq2:
        w.writerow([quality]+list(rq2[quality].values()))

rq2raw = pickle.load(open("RQ2stats.pkl","rb"))

for quality in rq2raw:
    with open(quality+'RQ2.csv','a') as rw:
        w = csv.writer(rw)
        w.writerow(['subject','fid','Qtype','response'])
        for subject in rq2raw[quality]:
            for fid in rq2raw[quality][subject]:
                for query in rq2raw[quality][subject][fid]:
                    if len(rq2raw[quality][subject][fid][query])>0:
                        for response in rq2raw[quality][subject][fid][query]:
                            w.writerow([subject,fid,query.replace('Query',''),response])



