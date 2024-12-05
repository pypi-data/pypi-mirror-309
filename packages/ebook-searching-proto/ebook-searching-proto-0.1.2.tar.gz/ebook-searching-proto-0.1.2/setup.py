from setuptools import setup, find_packages

setup(
    name='ebook-searching-proto',
    version='0.1.2',
    packages=find_packages(where="generated/proto"),
    package_dir={'': 'generated/proto'},
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    install_requires=[
        'grpcio',
        'protobuf',
    ],
    description='Generated protobuf and gRPC code',
    url='https://github.com/levandattt/EBOOK_Search_OWL',
    author='Chu',
    author_email='truongquangchu.tqc@gmail.com',
)
