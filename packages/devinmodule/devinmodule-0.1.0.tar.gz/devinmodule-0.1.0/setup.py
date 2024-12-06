from setuptools import setup, find_packages

setup(
    name='devinmodule',                  # Package name
    version='0.1.0',                   # Version
    description='A simple greetings module',
    author='Devin Mathew',
    author_email='devin@gofreelab.com',
    packages=find_packages(),          # Automatically find modules
    python_requires='>=3.6',           # Python version requirement
)