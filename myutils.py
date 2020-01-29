import sys
import javalang
from timeit import default_timer as timer

start = 0
end = 0

def prep(msg):
    global start
    sys.stdout.write(msg)
    sys.stdout.flush()
    start = timer()

def drop():
    global start
    global end
    end = timer()
    sys.stdout.write('done, %s seconds.\n' % (round(end - start, 2)))
    sys.stdout.flush()

def print_ast(tree):
    for path, node in tree:
        print(path, node)
