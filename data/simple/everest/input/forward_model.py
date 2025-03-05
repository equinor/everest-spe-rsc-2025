#!/usr/bin/env python
"""
Script that computes simple objective function.
"""

import json
import numpy as np
import argparse

def read_control(filename):
	""" Read control variables """
	with open(filename, 'r') as f:
		param = json.load(f) 
	return param

def simple(x,y):
    """ Simple function """
    return np.sin(np.pi*x)*np.sin(np.pi*y)

parser = argparse.ArgumentParser(description='Simple objective function')
parser.add_argument('-i', '--input', type=str, help='Input JSON file with x and y coordinates')
parser.add_argument('-o', '--output', type=str, help='Output text file with objective value')
args = parser.parse_args()

coordinates = read_control(args.input) 
z = simple(coordinates['x'], coordinates['y'])

with open(args.output, 'w') as g:
	g.write(str(z))
