#/usr/bin/env python
#-*- coding: utf-8 -*-
"""
    lights.py
    ~~~~~~~~~~~~~~~

    example : scan MText and MLeader on draw

    :copyright: (c) 2012 by Roman Haritonov.
    :copyright: (c) 2025 by obook.    
    :license: BSD, see LICENSE.txt for more details.
"""
import re
import sys
from collections import namedtuple, defaultdict

from pyzwcad import ZwCAD, utils

LampEntry = namedtuple('LampEntry', 'number, mark, numxpower')

# \A1;2ARCTIC SMC/SAN 254 \S2х54/2,5;\P300 лк
# '1/MARK1/23/LED;'
def iter_lamps(zwcad, objects):
    for obj in zwcad.iter_objects(('MText'), block=objects):  # 'MText', 'MLeader'
        print(obj)
        try:
            text = obj.TextString
        except Exception:
            continue
        
        '''
        debug
        '''
        
        # text = r'\A1;2ARCTIC SMC/SAN 254 \S2х54/2,5;\P300'
        
        print(f"IN   = [{text}]")
        
        
        text = utils.unformat_mtext(text)

        print(r"EXPECT [2ARCTIC SMC//AN 254 \S2х54/2,5;\P300]")
        
        print(f"OUT  = [{text}] (unformat_mtext)")
        
    
        
        # m = re.search(r'(?P<num>\d+)(?P<mark>.*?)\\S(?P<num_power>.*?)/.*?;', text)
        m = re.search(r'(?P<num>\d+)(?P<mark>.*?)\/(?P<num_power>.*?)\/.*?;', text)
        
        print("m=",m)
        if not m:
            continue
        print(m.group('num'), m.group('mark'), m.group('num_power'))
        yield LampEntry(m.group('num'), m.group('mark'), m.group('num_power'))

def main():
    zwcad = ZwCAD()
    try:
        zwcad.prompt("Lights counter\n")
    except Exception as error:
        print(f"ZwCAD error {error}")
        return
        
    objects = None
    if 'i' in sys.argv[1:]:
        objects = zwcad.get_selection('Select objects')
    lamps = defaultdict(int)
    for lamp in iter_lamps(zwcad, objects):
        lamps[lamp.mark] += int(lamp.number)
    print('-' * 79)
    for mark, number in sorted(lamps.items()):
        print('%-20s | %s' % (mark, number))

if __name__ == "__main__":
    with utils.timing():
        main()
