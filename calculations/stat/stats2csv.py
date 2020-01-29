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
        w.writerow(['subject']+list(range(40)))
        for subject in stats[quality]:
            del stats[quality][subject]['neutral']
            w.writerow([subject]+list(stats[quality][subject].values()))

rq2 = pickle.load(open("RQ2mean.pkl","rb"))

with open('RQ2mean.csv','a') as r:
    w = csv.writer(r)
    w.writerow(['questions']+list(rq2['accurate'].keys()))
    for quality in rq2:
        w.writerow([quality]+list(rq2[quality].values()))

rq2raw = pickle.load(open("RQ2stats.pkl","rb"))

with open('RQ2raw.csv','a') as raw:
    w = csv.writer(raw)
    w.writerow(['questions']+list(rq2raw['accurate'].keys()))
    for quality in rq2raw:
        w.writerow([quality]+list(rq2raw[quality].values()))

