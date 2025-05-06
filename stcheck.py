import re
import os
import sys
from typing import List, Tuple
from urllib.parse import urlparse

######################################
# Description: ST_duplicate Checker  #
# Date Creation: 10/23/2023          #
# Last update: 08/2/2024             #
# Author: @l0n3m4n                   #
# Version: v0.1                     #
######################################

 
class COLORS:
    LIGHTGREEN = "\033[92m"
    LIGHTRED = "\033[91m"
    LIGHTYELLOW = "\033[93m"
    LIGHTBLUE = "\033[94m"
    LIGHTCYAN = "\033[96m"
    RESET = "\033[0m"
 
def extract_urls(line: str) -> List[str]:
    """Extract URLs regex"""
    url_pattern = re.compile(
    r'http(?:s)?://'                         # http or https
    r'(?:www\.)?'                            # match www
    r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}'     # match domain amd subdomains
    r'(?:/[^\s]*)?'                          # optionally match path
)
    return url_pattern.findall(line)

def validate_url(url: str) -> bool:
    """Validate urls"""
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)

def process_file(file_path: str) -> Tuple[int, int, List[str], int]:
    """check for errors, warnings and duplicate links"""
    errors = []
    duplicate_links = set()
    url_set = set()
    total_urls = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                urls = extract_urls(line)
                total_urls += len(urls)
                for url in urls:
                    if not validate_url(url):
                        errors.append(f"{COLORS.LIGHTRED}Invalid URL: {url}{COLORS.RESET}")
                    if url in url_set:
                        duplicate_links.add(url)
                    url_set.add(url)
    except FileNotFoundError:
        print(f"{COLORS.LIGHTRED}Error: {COLORS.LIGHTGREEN}File '{file_path}' not found{COLORS.RESET}")
        sys.exit(1)
    except IOError as e:
        print(f"{COLORS.LIGHTRED}Error: {COLORS.LIGHTGREEN}Unable to read file '{file_path}': {e}{COLORS.RESET}")
        sys.exit(1)

    return len(errors), len(duplicate_links), list(duplicate_links), total_urls


def main():
    """main function to execute ST logic"""
    banner = f"""{COLORS.LIGHTGREEN}
  _______                         __     _______               __ __     __ __   
 |     __|.-----.---.-.----.----.|  |--.|_     _|.-----.-----.|  |  |--.|__|  |_ 
 |__     ||  -__|  _  |   _|  __||     |  |   |  |  _  |  _  ||  |    < |  |   _|
 |_______||_____|___._|__| |____||__|__|  |___|  |_____|_____||__|__|__||__|____|
 
            {COLORS.LIGHTCYAN}Author: l0n3m4n | Version: v0.2 | Check Duplicates Links                                                                           
    {COLORS.RESET}"""
    print(banner)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    url_file = os.path.join(script_dir, '.', 'README.md')
    url_file = os.path.normpath(url_file)


    if not os.path.isfile(url_file) or not os.access(url_file, os.R_OK):
        print(f"{COLORS.LIGHTRED}❗ {COLORS.RESET} {COLORS.LIGHTGREEN}URL file '{url_file}' not found or is not readable{COLORS.RESET}")
        sys.exit(1)

    if os.path.getsize(url_file) == 0:
        print(f"{COLORS.LIGHTRED}❗ {COLORS.RESET} {COLORS.LIGHTGREEN}URL file '{url_file}' is empty{COLORS.RESET}")
        sys.exit(1)
    
    try:
        search_term = input(f"{COLORS.LIGHTGREEN}Search specific toolname:{COLORS.RESET} ").strip()
        found_any = False

        if search_term:
            with open(url_file, 'r', encoding='utf-8') as file:
                for line in file:
                    if search_term.lower() in line.lower():
                        urls = extract_urls(line)
                        if urls:
                            found_any = True
                            print(f"\n{COLORS.LIGHTCYAN}Links containing '{COLORS.LIGHTGREEN}{search_term}{COLORS.RESET}':{COLORS.RESET}")
                            for url in urls:
                                print(f"{COLORS.LIGHTYELLOW}✅ {COLORS.RESET} {url}")

            if not found_any:
                print(f"\n{COLORS.LIGHTCYAN}No links found containing {COLORS.LIGHTGREEN}'{search_term}'{COLORS.RESET}")

        errors_count, duplicates_count, duplicate_links, total_urls = process_file(url_file)

        if errors_count:
            print(f"{COLORS.LIGHTRED} {errors_count}:{COLORS.RESET}")
            for error in errors_count:
                print(f"❌ {error}")
        else:
            print(f"\n{COLORS.LIGHTGREEN}No errors found{COLORS.RESET}")

        if duplicates_count:
            print(f"\n{COLORS.LIGHTRED}Duplicate Links{COLORS.RESET}: {COLORS.LIGHTGREEN}{duplicates_count}{COLORS.RESET}\n")
            for link in duplicate_links:
                print(f"- {link}")
        else:
            print(f"{COLORS.LIGHTGREEN}No duplicate links found{COLORS.RESET}")

        print(f"\n{COLORS.LIGHTBLUE}Total URLs{COLORS.RESET}: {COLORS.LIGHTGREEN}{total_urls}{COLORS.RESET}")
    except KeyboardInterrupt:
        print(f"\n{COLORS.LIGHTRED}User interruption: {COLORS.LIGHTGREEN}Session terminated.{COLORS.RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
