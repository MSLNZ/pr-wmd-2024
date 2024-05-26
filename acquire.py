import logging
import sys
from time import perf_counter

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d -- %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO,
)

import requests

from equipment import HP34401A

logger = logging.getLogger(__name__)

try:
    a, b, c = HP34401A('a'), HP34401A('b'), HP34401A('c')
except Exception as e:
    input(str(e))
    sys.exit(-1)

a.configure('acv', range=100, nsamples=1, auto_zero=True)
b.configure('aci', range=0.1, nsamples=1, auto_zero=True)
c.configure('aci', range=0.1, nsamples=1, auto_zero=True)

try:
    while True:
        logger.info('trigger')
        t1 = perf_counter()
        a.initiate()
        b.initiate()
        c.initiate()

        logger.info('fetching...')
        a_ureal = a.fetch()
        b_ureal = b.fetch()
        c_ureal = c.fetch()

        t2 = perf_counter()
        logger.info(f'took {t2-t1:.3f} seconds')

        # send data to webapp
        data = {
            'voltage': [a_ureal.x, a_ureal.u],
            'current1': [b_ureal.x, b_ureal.u],
            'current2': [c_ureal.x, c_ureal.u],
        }
        reply = requests.put('http://127.0.0.1:8050/update', json=data)

except (KeyboardInterrupt, OSError):
    pass
finally:
    a.disconnect()
    b.disconnect()
    c.disconnect()
