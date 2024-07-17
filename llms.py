from langchain_community.llms.ollama import Ollama
from langchain.prompts import ChatPromptTemplate
from json import JSONDecodeError
import json
from Prompt_Templates import PROMPT_TEMPLATE, PROMPT_TEMPLATE_ORG, PROMPT_TEMPLATE_ORG_SEMANTIC



model1 = "gemma2:9b"
#llms llama3:8b, mistral, gemma:7b, zephyr, mixtral:8x7b phi3:medium qwen2:7b
def llm(j):
    list = []
    for i in range(len(j['dataset'])):
        text = j['dataset'][i]['text']
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=text)
        model = Ollama(model=model1)
        response_text = f"""{model.invoke(prompt)}"""
#        print("\nllm", response_text)
        names = textSeperator(response_text)
        list.append(names)
    return list

def text_checking(text):
#    text.replace("'", "\'")
    text.replace("’","")
    if text.find('[') == -1 or text.find(']') == -1 or text.find('"') == -1 == -1:
        model = Ollama(model="qwen2:7b")
        #'---I want it in a format ["name1","name2"].provide only the list between the []. Dont forget ""between the names.'
        new_prompt = text + '---I want it in a format ["name1","name2"].provide only the list between the []. Dont forget ""between the names.'
        text = f"""{model.invoke(new_prompt)}"""
#        print("llm2",text)
#     if text.find('[') == -1 or text.find(']') == -1 or text.find('"') == -1 == -1:
#         model = Ollama(model="qwen2:7b")
#         new_prompt = text + '---I want it in a format ["name 1","name 2"].provide only the list between the []. Dont forget ""between the names. It is important to provide only 1 list'
#         text = f"""{model.invoke(new_prompt)}"""
        #print("llm3",text)
    if text.find('{'):
        text = text.replace("{", " ")
    if text.find('}'):
        text = text.replace("}", " ")
    if text.find('[['):
        text = text.replace("[[", "[")
    if text.find('[]'):  
        text = text.replace("[]", " ")
    if text.find("'"):
        text = text.replace("'", '')
    if text.find('\n'):
        text.replace("\n", "")
    return text

def textSeperator(text):
    text=text_checking(text)
    
    start_index = text.find('[')
    end_index = text.find(']') + 1
    # Extract the JSON list as a substring
    json_list_str = text[start_index:end_index]
#    print(json_list_str)
    # Convert the JSON list string to a Python list
    try:
        names = json.loads(json_list_str)
    except json.JSONDecodeError:
        print("json error")
        return []
    #print(names)
    return names


#------------------------------------------------------------------------------------------------------------------

def llm_org(j,ground_truth):
    list = []
    #initialize empty list and populate it with llm results 
    for i in range(len(j['dataset'])):
        text = j['dataset'][i]['text']
        
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_ORG)
        prompt = prompt_template.format(context=text)
        model = Ollama(model=model1)
        response_text = f"""{model.invoke(prompt)}"""
        response_text = remove_parentheses(response_text)
        
        #isolate the llm list and load in python
        names = textSeperator(response_text)
        
        #replace simalar semantically elements from llm list as they appear in ground truth list
        names = llm_semantic2(ground_truth,names,i)
#        print(names)
        list.append(names)
    return list


import re

def remove_parentheses(text):
    # Use a regular expression to find and remove parentheses and the text inside them
    return re.sub(r'\([^)]*\)', '', text)

def llm_semantic2(ground_truth,names,i):
    #the llm list
    llmlist = names
    #ground truth list
    ground_truth = ground_truth[i]
    ground_truth = str(ground_truth)
    #llm list
    names = str(names)

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_ORG_SEMANTIC)
    prompt = prompt_template.format(l1=ground_truth, l2=names)
    model = Ollama(model=model1)
    response_text = f"""{model.invoke(prompt)}"""

    #load the 2 semantically meaning list with common elements (not exactly match)
    l1g_from_match, l2n_from_match = matching_lists(response_text)

    #replace the matching elements on the actual llm list 
    llmlist_replaced = list_replacer(l1g_from_match, l2n_from_match, llmlist)
    return llmlist_replaced



def matching_lists(text):
    # Split the text into lines and remove the header and delimiter lines
    lines = text.strip().split('\n')[2:]

    # Initialize the lists
    list1 = []
    list2 = []

    # Process each line to extract elements
    for line in lines:
        elements = line.strip('|').split('|')
        list1.append(elements[0].strip())
        list2.append(elements[1].strip())

    #Should be conversaly to match the order of semantically meaning template 
    return list2, list1


def list_replacer(list1g, list2n, llmlist):
    #remove by chance " " at the end of the elements of llmlist  
    llmlist = [org.strip() for org in llmlist]
    
    #check if the 2 matching lists are the same size
    if len(list1g) == len(list2n):
        #iterate the lists
        for i in range(len(list1g)):
            #if the element corresponding to llm matcing lists found on the actual llmlist
            if list2n[i] in llmlist:
                #replace the element with the corresponding to ground truth matching list
                index_of_llm = llmlist.index(list2n[i])
                llmlist[index_of_llm] = list1g[i]

    return llmlist
            
    
    



