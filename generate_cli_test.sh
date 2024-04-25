#!/bin/bash

# This script is used to generate the output file for the CLI tests.

if [ $# -eq 0 ]; then
	echo "Usage: ./generate <in_file_name>"
	exit 1
fi

readonly base_path=test/cli
readonly in_path=$base_path/in/$1.txt
readonly out_path=$base_path/out/$1.txt

python3 computorv2.py < $in_path > $out_path 2>&1
