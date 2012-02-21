#!/usr/bin/env python
import statemachineregex
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('positionals', nargs='+')
args = parser.parse_args()
if len(args.positionals) == 2:
    s = open(args.positionals[1]).read()
else:
    s = sys.stdin.read()
print args.positionals
statemachineregex.demo_regex(args.positionals[0], s)
