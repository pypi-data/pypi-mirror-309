from setuptools import setup,find_packages

setup(
    name='FREEZINGEYES_STT',
    version='1.0.2',
    author='FreezingEYES',
    author_email='manthanrauthan1@gmail.com',
    description= 'Contain only one command which is > listen() > It just listenss',
)
packages = find_packages(),
install_requirements = [
    'selenium',
    'webdriver-manager',
]



