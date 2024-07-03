from langchain_community.llms.ollama import Ollama
from langchain.prompts import ChatPromptTemplate
from json import JSONDecodeError
import json
#You are an extremely careful and powerful name entity recognition agent, specialized on people!
# You are a Name Entity Recognition agent, working in a financial corruption tracing organization!
#Think step by step
#You are name entity recognizer, that you only need to identify individuals.  even if they are not important   Your final answer should be the list you concluded its correct!
PROMPT_TEMPLATE = """
    You are a Name Entity Recognition agent, working in a financial corruption tracing organization!
    your task is to extract all the people mentioned in the text! 
    At the end you will provide a list containing all the mentioned people ONLY THEIR NAMES. 
    Example ["name 1","name 2"]
    KEEP ONLY THE TEXT BETWEEN []
    Do not include any notes just a list with the names
    Do not forget to add the names between ""
    Think step by step
    ---

    {context}

    ---

    """
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
    text.replace("'", "\'")
    text.replace("’","\’")
    # if text.find('[') == -1 or text.find(']') == -1 or text.find('"') == -1 == -1:
    #     model = Ollama(model=model1)
    #     #'---I want it in a format ["name1","name2"].provide only the list between the []. Dont forget ""between the names.'
    #     new_prompt = text + '---I want it in a format ["name1","name2"].provide only the list between the []. Dont forget ""between the names.'
    #     text = f"""{model.invoke(new_prompt)}"""
    #     print("llm2",text)
    # if text.find('[') == -1 or text.find(']') == -1 or text.find('"') == -1 == -1:
    #     model = Ollama(model="qwen2:7b")
    #     new_prompt = text + '---I want it in a format ["name 1","name 2"].provide only the list between the []. Dont forget ""between the names. It is important to provide only 1 list'
    #     text = f"""{model.invoke(new_prompt)}"""
    #     print("llm3",text)
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
        text.replace("\n", " ")   
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

PROMPT_TEMPLATE_ORG = """
    your task is to extract all the Organizations mentioned in the text! At the end you will provide a list containing all the mentioned organizations ONLY THEIR NAMES. 
    Example ["org 1","org 2"]
    Do not include any counrty such as USA, Belgium, United Arab Emirates (UAE)!
    Do not provide abstract names such as "a russian company"
    Keep the full name
    An organization is an entity—such as a company, an institution (formal organization), or an association—comprising one or more people and having a particular purpose.
    ---

    {context}

    ---

    """

def llm_org(j):
    list = []
    for i in range(len(j['dataset'])):
        text = j['dataset'][i]['text']
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_ORG)
        prompt = prompt_template.format(context=text)
        model = Ollama(model=model1)
        response_text = f"""{model.invoke(prompt)}"""
        response_text = remove_parentheses(response_text)
        print("\nResponse",response_text)
        names = textSeperator(response_text)
        list.append(names)
    return list


import re

def remove_parentheses(text):
    # Use a regular expression to find and remove parentheses and the text inside them
    return re.sub(r'\([^)]*\)', '', text)

# # Example usage
# input_text = "International Emergency Economic Powers Act (IEEPA)"
# output_text = remove_parentheses(input_text)
# print("Before:", input_text)
# print("After:", output_text)





