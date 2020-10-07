def deduplicate(dup_list):
    result = []
    for item in dup_list:
        if item.attribute_name not in [i.attribute_name for i in result]:
            result.append(item)
    return result
