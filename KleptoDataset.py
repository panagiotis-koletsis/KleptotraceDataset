
import json
from scores import calculate_f1_score ,calculate_score
from llms import llm
import time




def load_data():
    path = '/home/kpanag/Downloads/Kleptotrace Dataset.json'
    with open(path) as f:
        j = json.load(f)
#        print(j)
        return j
def main():
    start_time = time.time()
    print("main")
    j=load_data()
    accT, preT, reT, f1T = [], [], [], []
    for k in range(7):
        print(k,"epoch")
        llmList = llm(j)
#        print(llmList)
        groundTruth = []
        for i in range(len(j['dataset'])):
            groundTruth.append(j['dataset'][i]['name_entities'])
#           print(j['dataset'][i]['name_entities'])
#        print(groundTruth)
#        score = calculate_f1_score(llmList, groundTruth)  # COMPARE lists as strings
#        print("F1 Score:", score[0],"\nPresicion:",score[1],"\nRecall:",score[2])
        acc, pre, re, f1 = calculate_score(groundTruth, llmList)
        print('accuracy=', acc, ', precision=', pre, ', recall=', re, ', f1=', f1)
        accT.append(acc), preT.append(pre), reT.append(re), f1T.append(f1)
    a = sum(accT)/len(accT)
    p = sum(preT)/len(preT)
    r = sum(reT)/len(reT)
    f = sum(f1T)/len(f1T)
    print("After iterations: ",k+1)
    print("accuracy:",a,"\nprecision:",p,"\nrecall:",r,"\nf1:",f)
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()

