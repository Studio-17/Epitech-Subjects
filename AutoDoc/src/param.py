def parse_param(args : list[str], valid_flags : dict[str, int], source :str) -> tuple:
    res = [" " for i in valid_flags.values() if i[0] >= 0]
    i = 1
    while (i < len(args)):
        if args[i] not in valid_flags.keys():
            raise ValueError(f"Invalid parameter {args[i]}")
        if (args[i] == '-h'):
            display_help(source)
        value = valid_flags[args[i]][0]
        nb_arguments = valid_flags[args[i]][1]
        match nb_arguments:
            case(1):
                res[value] = args[i + 1]
                i += 1
            case(0):
                res[value] = True
        i += 1 
    return tuple(res)

def display_help(source :str):
    with open(f"AutoDoc/help/help_{source}.txt", "r") as f:
        print(f.read())
    exit(0)