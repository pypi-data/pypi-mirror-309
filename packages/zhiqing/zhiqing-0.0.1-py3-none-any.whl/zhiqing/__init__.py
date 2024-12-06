def min_repetend_length(inputs):
    l = len(inputs)
    for i in range(1, l):
        for j in range(i+1, l):
            if not (inputs[j-i] == inputs[j]):
                break
        else:
            return i
    return l
