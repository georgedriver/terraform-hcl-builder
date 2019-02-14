from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='hcl_builder',
    version='0.0.1',
    author_email="george9012@hotmail.com",
    description="Build terraform HCL/import CMD from data resource output_file.",
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/georgedriver/terraform-hcl-builder",
    install_requires=[
        'terrascript==0.6.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['hcl_builder=hcl_builder:main'],
    },
)
