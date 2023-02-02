import csv

from colored import attr, fg


def myreader(filename: str):
    """ Read csv file and return a list of lists """
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        your_list = list(reader)

    return (your_list)


def color_print(text1, color):
    print(f'{fg(color)}{text1}{attr("reset")}')


def color_print_log(header, color, text):
    print(f'{fg(color)}{header:}{attr("reset")}', text)
