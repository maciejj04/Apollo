def absoluteListDifference(list1: [], list2: []) -> []:
    if len(list1) != len(list2):
        raise Exception("Function support only equal length lists!")
    
    resList = []
    for i in range(0, len(list1)):
        resList.append(list1[i] - list2[i])

    return resList
