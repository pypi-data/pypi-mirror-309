from setuptools import setup,find_packages

setup(
    name='OwaisAamir-STT',
    version='1',
    author='Muhammad Owais Aamir',
    author_email='owaisaamir53@gmail.com',
    description='this is speech to text package create by Muhammad Owais Aamir'
)
packages = find_packages(),
install_requirements = [
    'selenium',
    'webdriver_manager'
]
