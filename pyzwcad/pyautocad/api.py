
from pyzwcad import api

ACAD =  api.ZCAD
Autocad = api.ZwCAD

for name in dir(api.ZCAD):
    if (name[:3] == 'IZc'):
        setattr(ACAD, 'IAc' + name[3:], getattr(api.ZCAD, name))
    elif (name[:2] == 'zc'):
        setattr(ACAD, 'ac' + name[2:], getattr(api.ZCAD, name))
    elif (name[:2] == 'Zc'):
        setattr(ACAD, 'Ac' + name[2:], getattr(api.ZCAD, name))
