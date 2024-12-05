from setuptools import setup, find_packages

with open('app/Readme.md', 'r') as f:
    l_desc = f.read()

    print (l_desc)

    setup(
        name='bojan',
        version='0.0.5',
        description='A simple logging library',
        author='Daniil Grydin',
        package_dir={'': 'app'},
        packages=find_packages(where='app'),
        long_description=l_desc,
        long_description_content_type='text/markdown',
        url="https://github.com/daniilgrydin/bojan.git",
        author_email="",
        license="MIT",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=[],
        extras_require={
            "dev": [
                "pytest>=7.0",
                "twine>=4.0.2",
            ],
        },
        python_requires='>=3.6'
    )