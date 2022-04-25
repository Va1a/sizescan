#!/usr/bin/env python3

import os
import argparse
from colorama import init, Fore, Back, Style
from halo import Halo

init(autoreset=True)
spinner = Halo(spinner='dots', text='Initializing')
parser = argparse.ArgumentParser(description='Look for the largest files.')
parser.add_argument('path', metavar='path', type=str, help='Path to look inside.')
parser.add_argument('--results', dest='result_count', type=int, help='Number of results to give.', default=10)
args = parser.parse_args()

discoveredFiles = []
inaccessible = []
sumspace = 0

def traverse(folder):
	global sumspace
	for root, dirs, files in os.walk(folder):
		spinner.text = f'{Fore.MAGENTA}Searching {Fore.WHITE}{root}...'
		for file in files:
			try:
				size = int(os.path.getsize(os.path.join(root, file)))
				discoveredFiles.append({'file': os.path.join(root, file), 'size': size})
				sumspace += size
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
spinner.text = f'{Fore.YELLOW}Sorting...'
discoveredFiles.sort(key=lambda item: item['size'], reverse=True)
spinner.succeed(f'{Fore.GREEN}Searched & Sorted!\n')
print(f'{Style.BRIGHT}{Fore.WHITE}Size Total of Directory {Fore.MAGENTA}{args.path}{Fore.WHITE}: {Fore.YELLOW}{prettySize(sumspace)}')
print(f'{Style.BRIGHT}{Fore.WHITE}Biggest Files: {Fore.YELLOW}(to see more specify --results argument)')
for i in range(args.result_count):
	if i > len(discoveredFiles)-1:
		break
	print(f'{Fore.CYAN}{i+1}. {Fore.WHITE}{discoveredFiles[i]["file"]} {Fore.CYAN}: {Fore.RED}{prettySize(discoveredFiles[i]["size"])}')
if inaccessible:
	input(f'{Fore.YELLOW}Inaccessible files encountered. Press enter to view.')
	print(f'\n{Style.BRIGHT}{Fore.WHITE}Inaccessible files {Fore.YELLOW}(not sure how big they are):')
	for index, i in enumerate(inaccessible):
		print(f'{Fore.CYAN}{index+1}. {Fore.WHITE}{i}')
		if index == 9:
			input(f'{Fore.YELLOW}There\'s more. {len(inaccessible) - index} inaccessible files remaining. Press enter to list them all.')
