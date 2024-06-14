from langchain_community.llms.ollama import Ollama
from langchain.prompts import ChatPromptTemplate
from json import JSONDecodeError
import json
#You are an extremely careful and powerful name entity recognition agent, specialized on people-individuals-person!
# You are a Name Entity Recognition agent, working in a financial corruption tracing organization!
#example ["John Doe","Maria Smith"]
PROMPT_TEMPLATE = """

    your task is to extract all the people mentioned in the text even if they are not important! At the end you will provide a list containing all the mentioned people ONLY THEIR NAMES. 
     example ["name 1","name 2"]
    Your final answer should be the list you concluded its correct!
    KEEP ONLY THE TEXT BETWEEN []
    Do not include any notes just a list with the names
    Do not forget to add the names between ""
    ---

    {context}

    ---

    """

#llms llama3:8b, mistral, gemma:7b, zephyr, mixtral:8x7b
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
        model = Ollama(model="llama3:8b")
        text = model.invoke(text + '---I want it in a format ["name1","name2"].provide only the list between the []. Dont forget ""between the names.')
#        print("llm 2---****** response",text,"\n---")
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
#    print(json_list_str)
    # Convert the JSON list string to a Python list
    try:
        names = json.loads(json_list_str)
    except json.JSONDecodeError:
        print("json error")
        return []
    #print(names)
    return names