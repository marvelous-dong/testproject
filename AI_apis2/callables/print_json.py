def json_dict(target_dict, dict_name, count=1, final_json_string=""):

    if count == 1:
        final_json_string += f"{dict_name} = "
    else:
        final_json_string += f"{'  ' * (count - 1)}{dict_name}: "

    final_json_string += "{\n"

    for i in target_dict:
        if type(target_dict[i]) in [str, int, list]:
            final_json_string += f"{'  ' * count}{i}: {target_dict[i]},\n"
        elif type(target_dict[i]) == dict:
            new_count = count + 1
            final_json_string += json_dict(target_dict[i], i, new_count)

    if count == 1:
        final_json_string += "}"
    else:
        final_json_string += f"{'  ' * (count - 1)}"
        final_json_string += "}\n"

    return final_json_string
