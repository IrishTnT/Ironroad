from pathlib import Path
from thefuzz import fuzz
from thefuzz import process
import json
import xml.etree.ElementTree as ET
import urllib
import urllib.request
import logging

# BETA BRANCH CODE.

# The structure of:
#   Function Declaration - %1%
#   Pre-initialising     - %2%
#   Initialising         - %3%
#   main                 - %4%
# is used here under advice.
# CTRL + F phrases are provided for each section.

version = "v0.3"

# Function Declaration, %1%