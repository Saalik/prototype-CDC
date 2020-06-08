import logging
import sys
import datetime
import time

from rainbowfs.logger import Logger

journal = logging.getLogger()
journal.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(formatter)

l = Logger('journal')

current_time = lambda: int(round(time.time() * 1000))

trId = 0

fmt = '%d:%s:%s:%s'

low = l.id_low
high = l.id_high
assert low <= high

