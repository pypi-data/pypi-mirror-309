from setuptools import setup

name = 'KeyisBClient'

setup(
    name=name,
    version='1.4.0.1.9',
    author="KeyisB",
    author_email="keyisb.pip@gmail.com",
    description=name,
    long_description='',
    long_description_content_type="text/markdown",
    url=f"https://github.com/KeyisB/libs/tree/main/{name}",
    include_package_data=True,
    package_dir={'': f'{name}'.replace('-','_')},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    license="MMB License v1.0",
    install_requires= ['KeyisBLogging', 'httpx', 'KeyisBClient-httpx', 'KeyisBClient-mmbp'],
)
