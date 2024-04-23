import difflib

d = difflib.Differ()

def get_the_difference(file_path_1: str,
                       file_path_2: str):
    
    with open(file_path_1, "r") as file1:
        lines_1 = file1.readlines()
    
    with open(file_path_2, "r") as file2:
        lines_2 = file2.readlines()

    # diff = difflib.unified_diff(lines_1, lines_2, lineterm='')
    diff = list(d.compare(lines_1, lines_2))

    return "".join(diff)

diff = get_the_difference(file_path_1='./example.csv', file_path_2='./example_2.csv')

print(diff)