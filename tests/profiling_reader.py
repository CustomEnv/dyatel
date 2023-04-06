import os
import sys
from pstats import Stats

stats = Stats(f'{os.getcwd()}/prof/combined.prof', stream=sys.stdout)
stats.print_stats()
