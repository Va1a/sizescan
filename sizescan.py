#!/usr/bin/env python3

import os
import argparse
import math
from halo import Halo

spinner = Halo(spinner='dots', text='Initializing')
parser = argparse.ArgumentParser(description='Look for the largest files.')
parser.add_argument('path', metavar='path', type=str, help='Path to look inside.')
parser.add_argument('--results', dest='result_count', type=int, help='Number of results to give.', default=10)
args = parser.parse_args()

discoveredFiles = []
inaccessible = []

def traverse(folder):
	for root, dirs, files in os.walk(folder):
		spinner.text = f'Searching {root}...'
		for file in files:
			try:
				discoveredFiles.append({'file': os.path.join(root, file), 'size': int(os.path.getsize(os.path.join(root, file)))})
			except FileNotFoundError:
				inaccessible.append(os.path.join(root, file))

	return [os.path.join(root, dir) for dir in dirs]

def prettySize(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"



dirqueue = [args.path]
spinner.start()
while dirqueue:
	for directory in dirqueue:
		dirqueue.extend(traverse(directory))
		dirqueue.remove(directory)
spinner.text = 'Sorting...'
discoveredFiles.sort(key=lambda item: item['size'], reverse=True)
spinner.succeed('Searched & Sorted!\n')
print('Biggest Files: (to see more specify --results argument)')
for i in range(args.result_count):
	if i > len(discoveredFiles)-1:
		break
	print(f'{i+1}. {discoveredFiles[i]["file"]} : {prettySize(discoveredFiles[i]["size"])}')	