from setuptools import setup,find_packages

setup(
    name='FREEZINGEYES_STT',
    version='1.0.1',
    author='FreezingEYES',
    author_email='manthanrauthan1@gmail.com',
    description='Simple Python Script to convert voice to text and save it in a file',
)
packages = find_packages(),
install_requirements = [
    'selenium',
    'webdriver-manager',
]



