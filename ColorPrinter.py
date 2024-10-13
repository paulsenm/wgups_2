def print_color(string, color):
    match color:
        case "red":
            return f"\033[31m{string}\033[0m"
        case "blue":
            return f"\033[34m{string}\033[0m"
        case "green":
            return f"\033[32m{string}\033[0m"      
        case "yellow":
            return f"\033[33m{string}\033[0m"         
        case "cyan":
            return f"\033[36m{string}\033[0m"          