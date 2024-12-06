from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='fiap_valteci-package',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib fiap_valteci',
    author='valteci',
    author_email='valtecijunior@gmail.com',
    url='https://github.com/valteci/',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
