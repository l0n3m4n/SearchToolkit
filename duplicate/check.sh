#!/bin/bash

#Author: L0N3M4N 

RED='\033[0;31m'    # Red color for errors
YELLOW='\033[1;33m' # Yellow color for warnings
GREEN='\033[0;32m'  # Green color for success
NC='\033[0m'        # No color (to reset)

# Define the file containing the list of URLs
url_file="README.md"

# Check if the file exists and is readable
if [ ! -f "$url_file" ]; then
  echo -e "${RED}Error:${NC} URL file '$url_file' not found or is not readable."
  exit 1
fi

# Check if the file is empty
if [ ! -s "$url_file" ]; then
  echo -e "${YELLOW}Warning:${NC} URL file '$url_file' is empty."
  exit 1
fi

# Sort the URLs, find duplicates, and count them
duplicate_count=$(sort -u "$url_file" | uniq -d | wc -l)

# Check if any duplicates were found 
if [ "$duplicate_count" -gt 0 ]; then
  echo -e "${RED}Duplicate links found.${NC} Total duplicates: ${YELLOW}$duplicate_count${NC}"
else
  echo -e "${GREEN}No duplicate links found.${NC}"
fi
