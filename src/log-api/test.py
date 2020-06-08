import logging
import sys

from rainbowfs.logger import Logger


root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

l = Logger('logs')

fmt = '{"data": "coucou %d"}'

########################################
low = l.id_low
n = l.append(fmt % 666)
assert l.get(n - 1) is None
n = l.append(fmt % 999)
assert l.get(n) is None

l.flush()
assert l.get(n - 1) == fmt % 666
assert l.get(n) == fmt % 999

for o in l.get_range(l.id_low, n):
    assert o is not None

n = l.flush()
assert l.id_low == low
assert l.id_high == low + 2

n = l.truncate()
assert l.id_high == l.id_low
o = l.get(n)
assert o is None


########################################
low = l.id_low
n = l.append(fmt % 666)
assert l.get(n) is None
l.flush(n)
assert l.id_high == low + 1
assert l.get(n) == fmt % 666
l.truncate(n)
assert l.id_low == low + 1
assert l.get(n) is None


########################################
n = l.append(fmt % 666)
assert l.get(n) is None
n = l.append(fmt % 999)
assert l.get(n) is None

l.flush(n - 1)
assert l.get(n - 1) == fmt % 666
assert l.get(n) is None

l.flush(n)
assert l.get(n - 1) == fmt % 666
assert l.get(n) == fmt % 999

l.truncate(n - 1)
assert l.get(n - 1) is None
assert l.get(n) == fmt % 999

l.truncate(n)
assert l.get(n - 1) is None
assert l.get(n) is None
