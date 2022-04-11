#!/usr/bin/python

# A lazy script to prototype vernier creation for my p100. All measurements in
# mm

import math
import svgwrite
from svgwrite import mm

# Some constants for p100
collar_diameter = 110

p_tick_size = collar_diameter * math.pi / 100
vernier_tick_size = p_tick_size * 9 / 10

# Sizes of the ticks on the p100 dial
p_major_tick_width = 1.25
p_minor_tick_width = 0.5

# y adjustment for size difference of tick marks
tick_offset = (p_major_tick_width - p_minor_tick_width) / 2

v_tens_tick_length = 9
v_fives_tick_length = 6
v_ones_tick_length = 3

# Colors
tick_color='white'
bg_color='black'


def draw_p100_tick(dwg, x, y, outer_width, inner_width):
    """
    Draws a nested tick
    """
    dwg.add(dwg.rect(
        (x*mm, y*mm),  # starting position
        (outer_width*mm, p_major_tick_width*mm),  # size
        fill=tick_color))
    # Draw interor fill on major ticks w/ thin white boxes for lining up zero to a minor tick on p100
    dwg.add(dwg.rect(
        (x*mm, (y + tick_offset) * mm),  # starting position
        (inner_width*mm, p_minor_tick_width*mm),  # size
        fill=bg_color))


def draw_vernier(dwg, x, y):
    """
    Draws a single instance of a vernier that contains 10 ticks over 9 ticks worth of the stock p100 dial

    :param dwg: instance of svgwrite.Drawing
    :param x: int, x offset
    :param y: int, y offset
    """
    # Draw major Ticks
    draw_p100_tick(dwg, x, y, v_tens_tick_length, v_fives_tick_length)

    # Make second major tick shorter to emphasize that it's the end, not the
    # start of a vernier
    draw_p100_tick(dwg, x, vernier_tick_size * 10 + y, v_fives_tick_length,
                   v_ones_tick_length)

    # Draw minor ticks
    for i in range(1, 10):
        draw_p100_tick(dwg, x, vernier_tick_size * i + y, v_ones_tick_length, v_ones_tick_length)

    # Draw fives ticks
    draw_p100_tick(dwg, x, vernier_tick_size * 5 + y, v_fives_tick_length,
                   v_ones_tick_length)


def main():
    dwg = svgwrite.Drawing('vernier.svg', height='200mm', width='100mm')

    # Draw a black background box
    dwg.add(dwg.rect(
        (0*mm, 0*mm),  # starting position
        (40*mm, 300*mm),  # size
        fill=bg_color))

    # Draw a series of verniers
    for i in range(0, 7):
        draw_vernier(dwg, 10, 10+(p_tick_size*10) * i)

    # Add a '*' to the vernier that I want to be used as the zero marker
    dwg.add(dwg.text('*', insert=(16*mm, (9 + p_tick_size*10 * 3 ) * mm),
                     stroke='none', fill=tick_color,
                     font_size='10mm', font_family="Helvetica", rotate=[90]))

    dwg.save()


if __name__ == "__main__":
    main()
