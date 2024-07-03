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

    acc="-"
    return acc, f1_score , precision , recall

def calculate_score(true, predicted):  #
    TPs = 0             # true positives TP (predicted entities that are correct)
    TPsFPs = 0          # true positives TP + false positives FP (predicted entities, counting correct and incorrect)
    TPsFPsFNs = 0       # TP+FP+FN (predicted entities (correct and incorrect) plus entities missed)
    TPsFNs = 0          # TP+FN (entities in ground truth)

    for i in range(len(true)):
        true_set = set(true[i])
        predicted_set = set(predicted[i])

        # Calculate the intersection and union of the two sets
        intersection = true_set.intersection(predicted_set)
        union = true_set.union(predicted_set)

        # mporoun na ypologistoun kai pio eykola, alla to afinw etsi analytika gia na katalaveis ti einai to kathe set
        # des edw: https://en.wikipedia.org/wiki/Precision_and_recall
        TPs += len(intersection)
        TPsFPs += len(predicted_set)
        TPsFPsFNs += len(union)
        TPsFNs += len(true_set)

    precision = TPs / TPsFPs
    recall = TPs / TPsFNs
    accuracy = (TPs*1.0/TPsFPsFNs)
    f1 = 2 * (precision * recall) / (precision + recall)
    return accuracy, precision, recall, f1
    