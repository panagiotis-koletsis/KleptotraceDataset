import spacy
from Prompt_Templates import PROMPT_TEMPLATE, PROMPT_TEMPLATE_ORG, PROMPT_TEMPLATE_ORG_SEMANTIC
from llms import llm_semantic2, matching_lists,list_replacer

def spacy_nlp(j):
    list = []
    nlp = spacy.load('en_core_web_sm')
    for i in range(len(j['dataset'])):
        text = j['dataset'][i]['text']
        doc = nlp(text)
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        list.append(names)
    return list



def spacy_nlp_org(j,ground_truth):
    org_list = []
    nlp = spacy.load('en_core_web_sm')  # Load the spaCy model once, outside the loop
    for i in range(len(j['dataset'])):
        text = j['dataset'][i]['text']
        doc = nlp(text)
        names = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
#        names = llm_semantic2(ground_truth, names, i)
#        print(names)
        org_list.append(names)
    return org_list


