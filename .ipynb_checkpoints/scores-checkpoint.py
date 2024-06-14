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

# def calculate_score(list 1, list 2):
    