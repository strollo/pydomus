#!/usr/bin/env python

# Used to resolve in the current path the library suorces
# Usage:
#   from .context import <Module>

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../pydomus')))

from Component import *
from Pattern import *


