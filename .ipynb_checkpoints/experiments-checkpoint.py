from llms import llm ,llm_org
from scores import calculate_f1_score, calculate_score, score_from_text

def ner_exp(j):
    groundTruth = []
    for i in range(len(j['dataset'])):
        groundTruth.append(j['dataset'][i]['name_entities'])
    accT, preT, reT, f1T = [], [], [], []
    for k in range(7):
        print(k,"epoch")
        llmList = llm(j)    
        acc, pre, re, f1 = calculate_score(groundTruth, llmList)
        print('accuracy=', acc, ', precision=', pre, ', recall=', re, ', f1=', f1)
        accT.append(acc), preT.append(pre), reT.append(re), f1T.append(f1)
    a = sum(accT)/len(accT)
    p = sum(preT)/len(preT)
    r = sum(reT)/len(reT)
    f = sum(f1T)/len(f1T)
    print("After iterations: ",k+1)
    print("accuracy:",a,"\nprecision:",p,"\nrecall:",r,"\nf1:",f)

def org_exp(j):
    groundTruthOrg = []
    for i in range(len(j['dataset'])):
        groundTruthOrg.append(j['dataset'][i]['organizations'])
    print(groundTruthOrg) 
    preT, reT, f1T = [], [], []
    for k in range(1):
        print(k,"epoch")
        llmListOrg = llm_org(j)   
        print(llmListOrg)
        acc, pre, re, f1 = calculate_score(groundTruthOrg, llmListOrg)
        print('accuracy=', acc, ', precision=', pre, ', recall=', re, ', f1=', f1)
        preT.append(pre), reT.append(re), f1T.append(f1)
    p = sum(preT)/len(preT)
    r = sum(reT)/len(reT)
    f = sum(f1T)/len(f1T)
    print("After iterations: ",k+1)
    print("accuracy:","-","\nprecision:",p,"\nrecall:",r,"\nf1:",f)
    
    # llmListOrg = llm_org(j) 
    # acc, pre, re, f1 = calculate_score(groundTruthOrg, llmListOrg)
    print('accuracy=', acc, ', precision=', pre, ', recall=', re, ', f1=', f1)