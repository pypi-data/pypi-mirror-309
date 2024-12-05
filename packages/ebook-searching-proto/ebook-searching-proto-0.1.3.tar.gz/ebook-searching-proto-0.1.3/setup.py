from setuptools import setup, find_packages
from setuptools import find_packages
print("find_packages: ")
print(find_packages(where="generated"))

setup(
    name='ebook-searching-proto',
    version='0.1.3',
    packages=find_packages(where="generated"),  # Find all packages in 'generated'
    package_dir={'': 'generated'},  # Map root package to 'generated'
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    package_data={
        '': ['proto/*.py'],  # Explicitly include .py files in the 'proto' folder
    },
    install_requires=[
        'grpcio',
        'protobuf',
    ],
    description='Generated protobuf and gRPC code',
    url='https://github.com/levandattt/EBOOK_Search_OWL',
    author='Chu',
    author_email='truongquangchu.tqc@gmail.com',
)
