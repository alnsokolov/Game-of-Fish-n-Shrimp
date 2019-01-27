import sys
import argparse
from time import sleep
from random import choices

VOID, ROCK, FISH, SHRIMP = 0, 1, 2, 3

def get_surrounding_things(x, y, cur_iter):
    left, right = max(x - 1, 0), min(x + 1, len(cur_iter[0]) - 1)
    top, bottom = max(y - 1, 0), min(y + 1, len(cur_iter) - 1)
    surroundings = [cur_iter[y_hat][x_hat]
                        for x_hat in range(left,right + 1)
                            for y_hat in range(top,bottom+1)
                                if x_hat != x or y_hat != y]
    return surroundings.count(FISH), surroundings.count(SHRIMP)

def next_iter(cur_iter):
    rows, columns = len(cur_iter), len(cur_iter[0])
    new_iter = [[VOID]*columns for _ in range(columns)]

    for y in range(rows):
        for x in range(columns):
            cur_fish, cur_shrimp = get_surrounding_things(x, y, cur_iter)

            if cur_iter[y][x] == ROCK:
                new_iter[y][x] = ROCK
            elif cur_iter[y][x] == FISH:
                new_iter[y][x] = FISH if 2 <= cur_fish <= 3 else VOID
            elif cur_iter[y][x] == SHRIMP:
                new_iter[y][x] = SHRIMP if 2 <= cur_shrimp <= 3 else VOID
            else:
                if cur_fish == 3:
                    new_iter[y][x] = FISH
                elif cur_shrimp == 3:
                    new_iter[y][x] = SHRIMP

    return new_iter

def get_printable_text(cur_iter):
    mapped_arr = [[["🌊", "⛰️", "🐟", "🦐"][val] for val in line] for line in cur_iter]
    return "\n".join(map(" ".join, mapped_arr))

def print_delayed_text(text, delay):
    for char in text:
        print(char, end='')
        sys.stdout.flush()
        if char != "\n":
            sleep(delay)
    print()

def generate_field(height, width):
    arr = list(range(4))
    return [[choices(arr, [4, 2, 1, 1])[0] for x in range(width)] for y in range(height)]

def main():
    parser = argparse.ArgumentParser(description="Conways Game of Life cellular automaton with two species")
    parser.add_argument("--file", "-f",
                        help="Path to file seed of automaton")
    parser.add_argument("--iterations", "-i",
                        metavar="N", type=int,
                        help="Number of iterations to be simulated")
    parser.add_argument("--show", "-s",
                        metavar="[Y/N]",
                        help="Show process of simulation")
    args = parser.parse_args()
    
    field = None

    if args.file != None:
        file = open(args.file)
        field = [list(map(int, line.split())) for line in file.readlines()]
        file.close()
    else:
        field = generate_field(6, 6)

    print_delayed_text(get_printable_text(field), 0.03)
    print()
    
    if args.iterations != None:
        for i in range(args.iterations):
            field = next_iter(field)
            if (args.show.lower() == 'y' and i != args.iterations - 1):
                print_delayed_text(get_printable_text(field), 0.03)
                print()
    
    print("End state:")
    print_delayed_text(get_printable_text(field), 0.03)

if __name__ == "__main__":
    main()
