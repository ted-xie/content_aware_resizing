#!/bin/bash
set -e

python main.py -i inputs/mountains.jpg -nx 10 -ny 10 -o outputs/out_mountains.jpg

open outputs/out_mountains.jpg
