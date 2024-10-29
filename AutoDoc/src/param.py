def parse_param(args : list[str], valid_flags : dict[str, int], source : str) -> tuple:
    res = [" " for i in valid_flags.values() if i >= 0]
    i = 1
    while (i < len(args)):
        if args[i] not in valid_flags.keys():
            raise ValueError(f"Invalid parameter {args[i]}")
        if (args[i] == '-h'):
            display_help(source)
        value = valid_flags[args[i]]
        res[value] = args[i + 1]
        i += 2
    return tuple(res)

def display_help(source : str):
    with open(f"MarvinScrapper/help/help_{source}.txt", "r") as f:
        print(f.read())
    exit(0)