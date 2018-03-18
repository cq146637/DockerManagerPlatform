# -*- coding: utf-8 -*-
__author__ = 'CQ'


def search_more(string):
    global counter, digit
    for i in string:
        try:
            int(i)
            if i in digit:
                digit.append(i)
                counter.pop(i)
                key = ''.join(digit)
                print(key)
                if key in counter.keys():
                    counter[key] += 1
                else:
                    counter[key] = 1
            else:
                digit = []
                if i in counter.keys():
                    counter[i] += 1
                else:
                    counter[i] = 1
            digit.append(i)
        except ValueError:
            digit = []
            if i in counter.keys():
                counter[i] += 1
            else:
                counter[i] = 1


if __name__ == "__main__":
    counter = {}
    digit = []
    string = "9fil3dj11P0jAsf11j"
    print(string)
    search_more(string)
    print(counter)
