#!/usr/bin/env python3

from math import ceil, log, floor

import sys
from random import randint

from PIL import Image


def cellular_automata(init_state, rule):
    """
    Carries out a cellular automata with the given rule
    :param init_state: A list of states, the inital sate for this CA
    :param rule: A dict of {neighborhood: state} representing the cellular automata
    :return: Yields each generation one by one
    """
    w = len(init_state)
    prev_state = list(init_state)
    next_state = list(prev_state)
    while True:
        neighborhood = (prev_state[-1], prev_state[0], prev_state[1])
        next_state[0] = rule[neighborhood]
        for i in range(1, w-1):
            neighborhood = tuple(prev_state[i-1:i+2])
            next_state[i] = rule[neighborhood]
        neighborhood = (prev_state[w-2], prev_state[w-1], prev_state[0])
        next_state[w-1] = rule[neighborhood]

        # copy list for output since next_state, prev_state are swapped each generation
        yield list(next_state)
        tmp = prev_state
        prev_state = next_state
        next_state = tmp


def wolfram_rule(rule_num : int, states : int, neighbors=1):
    """
    Generate a rule form a number, given the nubmer of states and neighbors (to each side)
    :param rule_num:
    :param states:
    :param neighbors:
    :return:
    """
    neighborhood_size = 2 * neighbors + 1
    possible_neighborhoods = states ** neighborhood_size
    rule_string = expand_base(rule_num, states, places=possible_neighborhoods)
    if len(rule_string) > possible_neighborhoods:
        raise ValueError("Rule number is too big for number of states and neighborhood size.")
    neighborhoods = [expand_base(i, states, places=neighborhood_size) for i in range(possible_neighborhoods-1, -1, -1)]
    rule = {ns: s for ns, s in zip(neighborhoods, rule_string)}
    return rule


def expand_base(x, b, places=0):
    """
    Convert a number to a tuple of digits in the given base.
    :param x: The number
    :param b: The base
    :param places: The number of places....
    :return:
    """
    if x == 0:
        return (0,) * max(1, places)
    i = max(places, int(floor(log(x, b)))) - 1
    p = b ** i
    digits = []
    while i >= 0:
        d = int(x / p)
        digits.append(d)
        x -= p*d
        p /= b
        i -= 1
    return tuple(digits)


def ca_to_image(generations, color_map):
    """
    Converts a list of generations of cellular automata to an image
    :param generations:
    :param color_map:
    :return: A list of (R,G,B) tuples
    """
    height = len(generations)
    width = len(generations[0])
    out_pixels = [None] * (width * height)
    idx = 0
    for y in range(height):
        g = generations[y]
        for x in range(width):
            cell = g[x]
            out_pixels[idx] = color_map[cell]
            idx += 1
    return out_pixels


def main():
    """
    Given a rule, image width, number of generations, and output file, runs the cellular automata and saves the output. 
    The rule is specified in Stephen Wolfram's 1D cellular automata notation.
    """
    rule, width, n_generations, outfile = sys.argv[1:]
    rule, width, n_generations = map(int, [rule, width, n_generations])
    r = wolfram_rule(rule, states=2)
    init_state = [randint(0, 1) for _ in range(width)]
    generations = [init_state]
    n = 1
    for g in cellular_automata(init_state, r):
        n += 1
        if n > n_generations:
            break
        generations.append(g)

    default_color_map = {0: (255, 226, 131), 1: (246, 182, 106), 2: (230, 129, 106), 3: (230, 206, 172)}
    out_pixels = ca_to_image(generations, default_color_map)
    img_out = Image.new(mode="RGB", size=(width, n_generations))
    img_out.putdata(out_pixels)
    img_out.save(outfile, quality=120)


if __name__ == '__main__':
    main()
