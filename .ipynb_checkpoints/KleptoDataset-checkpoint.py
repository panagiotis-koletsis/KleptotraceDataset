from json import JSONDecodeError

import pandas as pd
from langchain_community.llms.ollama import Ollama
from langchain.prompts import ChatPromptTemplate
import json
PROMPT_TEMPLATE = """
    You are an extremely careful and powerful name entity recognition agent, specialized on people-individuals-person!
    your task is to extract all the people mentioned in the text even if they are not important! At the end you will provide a JSON list containing all the mentioned people ONLY THEIR NAMES. 
     example ["John Doe","Maria Smith"]
    Your final answer should be the list you concluded its correct!
    KEEP ONLY THE TEXT BETWEEN []
    Do not include any notes just a list with the names
    Do not forget to add the names between ""
    ---

    {context}

    ---

    """
def llm(j):
    list = []
    for i in range(len(j['dataset'])):
        text = j['dataset'][i]['text']
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=text)
        model = Ollama(model="llama3:8b")
        response_text = model.invoke(prompt)
#        print("llm response---",response_text,"\n---")
        names = textSeperator(response_text)
#        print(names)
        list.append(names)
        #print(response_text)
    return list

def text_checking(text):
    if text.find('[') == -1:  
        model = Ollama(model="mistral")
        text = model.invoke(text + '---is this a correct json list ? i want it in a format ["name1","name2"..].provide only the list between the []')
#        print("llm mistral---****** response",text,"\n---")
    if text.find('{'):
        text = text.replace("{", " ")
    if text.find('}'):
        text = text.replace("}", " ")
    if text.find('[['):
        text = text.replace("[[", "[")
    if text.find('[]'):  
        text = text.replace("[]", " ")
    if text.find("'"):
        text = text.replace("'", '"')
    if text.find('\n'):
        text.replace("\n", " ")
    return text

def textSeperator(text):
    text=text_checking(text)
    
    start_index = text.find('[')
    end_index = text.find(']') + 1
    # Extract the JSON list as a substring
    json_list_str = text[start_index:end_index]
    # Convert the JSON list string to a Python list
    try:
        names = json.loads(json_list_str)
    except json.JSONDecodeError:
        print("json error")
        return []
    #print(names)
    return names

def calculate_f1_score(list1, list2):
    #convert list of lists to string in order to calculate score 
    nested_strings = [', '.join(map(str, sublist)) for sublist in list1]
    text1 = ', '.join(nested_strings)

    nested_strings = [', '.join(map(str, sublist)) for sublist in list2]
    text2 = ', '.join(nested_strings)
    
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    # Calculate intersection (common words)
    common_words = words1.intersection(words2)

    # Calculate precision, recall, and F1 score
    precision = len(common_words) / len(words1)
    recall = len(common_words) / len(words2)

    if precision + recall == 0:
        f1_score = 0
    else:
        f1_score = 2 * (precision * recall) / (precision + recall)

    return f1_score , precision , recall

def load_data():
    path = '/home/kpanag/Downloads/Kleptotrace Dataset.json'
    with open(path) as f:
        j = json.load(f)
        return j
def main():
    print("main")
    j=load_data()
    llmList = llm(j)
#    print(llmList)
    groundTruth = []
    for i in range(len(j['dataset'])):
        groundTruth.append(j['dataset'][i]['name_entities'])
#        print(j['dataset'][i]['name_entities'])
#    print(groundTruth)
    score = calculate_f1_score(llmList, groundTruth)
    print("F1 Score:", score[0],"\nPresicion:",score[1],"\nRecall:",score[2])




if __name__ == "__main__":
    main()

