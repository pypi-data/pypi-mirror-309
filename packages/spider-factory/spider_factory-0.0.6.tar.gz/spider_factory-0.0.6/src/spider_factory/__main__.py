import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from spider_factory import SpiderClient

spider_client = SpiderClient()
spider_client.run_spider()