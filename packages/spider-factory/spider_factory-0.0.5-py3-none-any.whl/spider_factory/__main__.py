import os
import sys

import spider_factory

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from spider_factory import run_spider

run_spider()