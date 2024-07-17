
#Template for names of individuals and the trials of prompting best practices 
#------------------------------------------

#You are an extremely careful and powerful name entity recognition agent, specialized on people!
#You are a Name Entity Recognition agent, working in a financial corruption tracing organization!
#Think step by step
#You are name entity recognizer, that you only need to identify individuals.  even if they are not important   Your final answer should be the list you concluded its correct!
PROMPT_TEMPLATE = """
    You are an extremely careful and powerful name entity recognition agent, specialized on people!
    your task is to extract all the people mentioned in the text! 
    At the end you will provide a list containing all the mentioned people ONLY THEIR NAMES. 
    Example ["name 1","name 2"]
    KEEP ONLY THE TEXT BETWEEN []
    Do not include any notes just a list with the names
    Do not forget to add the names between ""
    ---

    {context}

    ---

    """
#------------------------------------------

#Template for organizations
#------------------------------------------

#An organization is an entity—such as a company, an institution (formal organization), or an association—comprising one or more people and having a particular purpose.
#Think step by step
#You are an extremely careful and powerful name entity recognition agent, specialized on organizations!
#You are a Name Entity Recognition agent, working in a financial corruption tracing organization!
#You are name entity recognizer, that you only need to identify organizations. Even if they are not important. Your final answer should be the list you concluded its correct!
PROMPT_TEMPLATE_ORG = """
    your task is to extract all the Organizations mentioned in the text! At the end you will provide a list containing all the mentioned organizations ONLY THEIR NAMES.
    Example ["org 1","org 2"]
    Do not include any countries such as USA, Belgium, United Arab Emirates (UAE)!
    Do not provide abstract names such as "a russian company"
    Keep the full name
    ---

    {context}

    ---

    """
#list 1 = ground truth l2 = llmlist           Template for matching elements
PROMPT_TEMPLATE_ORG_SEMANTIC = """
    List 2: {l2}
    List 1: {l1}
    ----Provide a table ONLY including all the semantically matching elements from list 2 to list 1
    example
    |element from list 2 | elements from list 1|
    

    Do not include any other notes. Provide only the list 

    """


