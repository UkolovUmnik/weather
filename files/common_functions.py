def merge_two_lists(list1:list,list2:list)->list:
    if list1 is None or list2 is None: return None
    if list1==[] and list2!=[]: return list2
    if list2==[] and list1!=[]: return list1
    list_end=[]
    for element in list1:
        list_end.append(element)
    for element in list2:
        if element not in list_end: 
            list_end.append(element)
    return list_end