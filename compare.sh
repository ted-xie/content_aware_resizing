#!/bin/bash

echo "Random statistics:"
python ssim.py inputs/mountains.jpg outputs/out_mountains_RANDOM.jpg

echo "Greedy statistics:"
python ssim.py inputs/mountains.jpg outputs/out_mountains_GREEDY.jpg

