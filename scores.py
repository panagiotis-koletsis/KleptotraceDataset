# def calculate_f1_score(list1, list2):
#     #convert list of lists to string in order to calculate score
#     nested_strings = [', '.join(map(str, sublist)) for sublist in list1]
#     text1 = ', '.join(nested_strings)
#
#     nested_strings = [', '.join(map(str, sublist)) for sublist in list2]
#     text2 = ', '.join(nested_strings)
#
#     words1 = set(text1.lower().split())
#     words2 = set(text2.lower().split())
#
#     # Calculate intersection (common words)
#     common_words = words1.intersection(words2)
#
#     # Calculate precision, recall, and F1 score
#     precision = len(common_words) / len(words1)
#     recall = len(common_words) / len(words2)
#
#     if precision + recall == 0:
#         f1_score = 0
#     else:
#         f1_score = 2 * (precision * recall) / (precision + recall)
#
#     acc="-"
#     return acc, f1_score , precision , recall
#
def calculate_score(true, predicted):  #
    TPs = 0.0             # true positives TP (predicted entities that are correct)
    TPsFPs = 0.0         # true positives TP + false positives FP (predicted entities, counting correct and incorrect)
    TPsFPsFNs = 0.0       # TP+FP+FN (predicted entities (correct and incorrect) plus entities missed)
    TPsFNs = 0.0          # TP+FN (entities in ground truth)

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
    accuracy = (TPs/TPsFPsFNs)
    f1 = 2 * (precision * recall) / (precision + recall)
    return accuracy, precision, recall, f1

# def score_from_text(l1, l2):
#     f1_scores = []
#     precisions = []
#     recalls = []
#
#     for i in range(len(l1)):
#         k1 = l1[i]
#         k2 = l2[i]
#         text1 = ' '.join(k1)
#         text2 = ' '.join(k2)
#         tokens1 = set(text1.split())
#         tokens2 = set(text2.split())
#
#         # Calculate True Positives (TP), False Positives (FP), and False Negatives (FN)
#         TP = len(tokens1.intersection(tokens2))
#         FP = len(tokens1 - tokens2)
#         FN = len(tokens2 - tokens1)
#
#         # Calculate Precision
#         precision = TP / (TP + FP) if (TP + FP) > 0 else 0
#
#         # Calculate Recall
#         recall = TP / (TP + FN) if (TP + FN) > 0 else 0
#
#         # Calculate F1 Score
#         if precision + recall == 0:
#             f1_score = 0.0
#         else:
#             f1_score = 2 * (precision * recall) / (precision + recall)
#
#         # print(f"F1 Score: {f1_score}")
#         # print(f"Precision: {precision}")
#         # print(f"Recall: {recall}")
#
#         f1_scores.append(f1_score)
#         precisions.append(precision)
#         recalls.append(recall)
#
#     avg_f1 = sum(f1_scores) / len(f1_scores) if f1_scores else 0
#     avg_precision = sum(precisions) / len(precisions) if precisions else 0
#     avg_recall = sum(recalls) / len(recalls) if recalls else 0
#     acc="-"
#     return acc, avg_f1, avg_precision, avg_recall
    