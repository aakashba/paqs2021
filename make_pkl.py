import pickle
import argparse
import os
from collections import OrderedDict

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--filename', type=str, default="ftagged.txt")
    args = parser.parse_args()
    filename = args.filename
    with open(filename, "r") as rawfile:
        interactions = OrderedDict()
        fqmap = OrderedDict()
        user = -1
        function = -1
        questions = None
        query = ""
        response = ""
        r1=''
        r2=''
        r3=''
        r4=''
        comment = ""
        for line in rawfile:
            if ":" in line:
                linetype, content = line.split(":", 1)
                if linetype == "User":
                    user = content.strip()
                elif linetype == "Function":
                    function = int(content)
                elif linetype == "Questions":
                    questions = [int(q.strip()) for q in content.strip().strip('][').split(',')]
                elif "Query" in linetype:
                    qno = linetype.strip()
                    query = content.strip()
                elif linetype == "Response":
                    response = content.strip()
                elif linetype == "Rating 1":
                    r1 = content.strip()
                elif linetype == "Rating 2":
                    r2 = content.strip()
                elif linetype == "Rating 3":
                    r3 = content.strip()
                elif linetype == "Rating 4":
                    r4 = content.strip()
                elif linetype == "User Comment":
                    comment = content.strip()
                    if user not in interactions: interactions[user] = OrderedDict()
                    if user not in fqmap: fqmap[user] = OrderedDict()
                    if function not in interactions[user]: interactions[user][function] = []
                    fqmap[user][function] = questions
                    interactions[user][function].append({qno: query, "response": response, 'r1': r1, 'r2':r2, 'r3':r3, 'r4':r4, 'comment': comment})
        
        if not os.path.exists("pkl/"+filename.split(".")[0]):
            os.mkdir("pkl/"+filename.split(".")[0])
            os.mkdir("pkl/"+filename.split(".")[0]+"/interactions")
            os.mkdir("pkl/"+filename.split(".")[0]+'/fqmap')
        pickle.dump(interactions, open("pkl/"+filename.split(".")[0]+"/interactions/"+"all"+".pkl", "wb"))
        pickle.dump(fqmap, open("pkl/"+filename.split(".")[0]+"/fqmap/"+"all"+".pkl", "wb"))
        for user in interactions:
            pickle.dump(interactions[user], open("pkl/"+filename.split(".")[0]+"/interactions/"+user.split("@")[0]+".pkl", "wb"))
            pickle.dump(fqmap[user], open("pkl/"+filename.split(".")[0]+"/fqmap/"+user.split("@")[0]+".pkl", "wb"))
