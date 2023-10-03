#!/bin/bash

# Author: L0N3M4N 
# Key features: Checking ERRORS, EMPTY, DUPLICATES, WARNINGS

# Define colors and text styles
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BOLD='\033[1m'
NC='\033[0m'

# Function to check if a file exists and is readable
file_exists_and_readable() {
  local file="$1"
  if [ ! -f "$file" ] || [ ! -r "$file" ]; then
    return 1
  else
    return 0
  fi
}

# Function to validate URLs using regex
validate_url() {
  local url="$1"
  # Only validate URLs with specific protocols: http, https, ftp, mailto
  local url_pattern="^(https?|ftp|mailto):\/\/[^\s/$.?#].[^\s]*$"
  if [[ $url =~ $url_pattern ]]; then
    return 0
  else
    return 1
  fi
}

# Function to print messages in color
print_message() {
  local message="$1"
  local color="$2"
  echo -e "${color}${message}${NC}"
}

# Define the file containing the list of URLs
url_file="README.md"

# Check if the file exists and is readable
if ! file_exists_and_readable "$url_file"; then
  echo -e "$YELLOW Error: URL file '$url_file' not found or is not readable. ${NC}"
  exit 1
fi

# Check if the file is empty
if [ ! -s "$url_file" ]; then
  echo -e "$YELLOW Error: URL file '$url_file' is empty. ${NC}" 
  exit 1
fi

# Initialize Markdown lists for errors, warnings, and duplicate links
errors="Errors:\n"
warnings="Warnings:\n"
duplicate_links="Duplicate Links:\n"
duplicate_count=0

# Extract URL from the file and validate them
while read -r line; do
  # Use a regex pattern to find URLs in the line
  urls=($(echo "$line" | grep -oE '(https?|ftp|mailto):\/\/[^ '"'"'"\t\n\r\f\v\[\]]+'))

  for url in "${urls[@]}"; do
    if ! validate_url "$url"; then
      errors+="- Invalid URL: ${BOLD}$url${NC}\n"
    fi
  done
done < "$url_file"

# Sort the URL, find duplicates, and count them
duplicate_links_list=$(grep -oP '(https?|ftp|mailto):\/\/[^ \t\n\r\f\v\[\]]+' "$url_file" | sort | uniq -d)

# Check if any duplicates were found 
if [ -n "$duplicate_links_list" ]; then
  IFS=$'\n' read -r -a duplicate_links_array <<< "$duplicate_links_list"
  for link in "${duplicate_links_array[@]}"; do
    duplicate_links+="- $link\n"
    ((duplicate_count++))
  done
else
  duplicate_links+="${GREEN}No duplicate links found.${NC}\n" # Green color for no duplicates found
fi

# Print the Markdown formatted output including the duplicate count
echo -e "${RED}$errors ${NC}\n${YELLOW}$warnings${NC}\n${GREEN}$duplicate_links ${NC}" 
echo -e "${GREEN}Duplicate Count:$duplicate_count" 
