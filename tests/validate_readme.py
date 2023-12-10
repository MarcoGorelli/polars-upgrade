from __future__ import annotations

import re

with open('README.md') as f:
    lines = f.readlines()


def find_line(lines, match):
    for (i, l) in enumerate(lines):
        if match in l:
            return i
    return None


versions = re.findall(r'Version (\d+\.\d+\.\d+)', ''.join(lines))
print(versions)

content = ''.join([line[2:] for line in lines if line.startswith('- ')])
with open('tmp.py', 'w') as f:
    f.write('import polars as pl\n' + content)
