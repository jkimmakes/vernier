#!/usr/bin/python

# A lazy script to prototype vernier creation for my p100. All measurements in
# mm

import math
import svgwrite
from svgwrite import mm

# Some constants for p100
collar_diameter = 110

p_tick_size = collar_diameter * math.pi / 100
vernier_tick_size = p_tick_size / 9 * 10

# Sizes of the ticks on the p100 dial
p_major_tick_width = 1.25
p_minor_tick_width = 0.5

# y adjustment for size difference of tick marks
tick_offset = (p_major_tick_width - p_minor_tick_width) / 2

v_tens_tick_length = 9
v_fives_tick_length = 6
v_ones_tick_length = 3

# Colors
tick_color='black'
bg_color='white'


def draw_vernier(dwg, x, y):
    """
    Draws a single instance of a vernier that contains 10 ticks over 9 ticks worth of the stock p100 dial

    :param dwg: instance of svgwrite.Drawing
    :param x: int, x offset
    :param y: int, y offset
    """
    # Draw major Ticks
    dwg.add(dwg.rect(
        (x*mm, y*mm),  # starting position
        (v_tens_tick_length*mm, p_major_tick_width*mm),  # size
        fill=tick_color))
    dwg.add(dwg.rect(
        (x*mm, (vernier_tick_size * 10 + y) * mm),
        (v_tens_tick_length*mm, p_major_tick_width*mm),
        fill=tick_color))

    # Draw minor ticks
    for i in range(2, 10):
        dwg.add(dwg.rect(
            (x*mm, (vernier_tick_size * i + y + tick_offset)*mm),
            (v_ones_tick_length*mm, p_minor_tick_width*mm),
            fill=tick_color))

    # Draw fives ticks
    dwg.add(dwg.rect(
        (x*mm,(vernier_tick_size * 5 + y + tick_offset)*mm),
        (v_fives_tick_length*mm, p_minor_tick_width*mm),
        fill=tick_color))

    # Draw interor fill on major ticks w/ thin white boxes for lining up zero to a minor tick on p100
    dwg.add(dwg.rect(
        (x*mm, (y + tick_offset) * mm),  # starting position
        (v_fives_tick_length*mm, p_minor_tick_width*mm),  # size
        fill=bg_color))
    dwg.add(dwg.rect(
        (x*mm, (vernier_tick_size * 10 + y + tick_offset) * mm),
        (v_fives_tick_length*mm, p_minor_tick_width*mm),
        fill=bg_color))


def main():
    dwg = svgwrite.Drawing('vernier.svg', height='200mm', width='100mm')

    for i in range(0, 7):
        draw_vernier(dwg, 10, 10+(p_tick_size*10) * i)

    dwg.save()


if __name__ == "__main__":
    main()
