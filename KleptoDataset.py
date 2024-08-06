import json
import time
from experiments import ner_exp ,org_exp
from experiments import spacy_exp, spacy_exp_org

def load_data():
    path = '/home/kpanag/Downloads/Dataset-org.json'
    with open(path) as f:
        j = json.load(f)
        return j
              
def main():
    start_time = time.time()
    print("main")
    j=load_data()
      
#    ner_exp(j)
    org_exp(j)
#    spacy_exp(j)
#    spacy_exp_org(j)
    
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
