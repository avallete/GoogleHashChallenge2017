import sys

def resolve(input):
    pass

def get_input(fd):
    lines = []
    for line in fd.readlines():
        lines.append(line.rstrip())
    return lines

def split_line(line):
    return [c for c in line]

def app_run():
    fd = open(sys.argv[1], "r")
    input = get_input(fd)
    pizza = []
    #(R, C, L, H) = input.pop(0).split(' ')
    for line in input:
        print (split_line(line))
        pizza.append(split_line(line))
    
    #import ipdb; ipdb.set_trace()
    fd.close()

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            app_run()
    except OSError as e:
        print("Error")
