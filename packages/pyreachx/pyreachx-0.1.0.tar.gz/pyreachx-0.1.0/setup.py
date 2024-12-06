from setuptools import setup, find_packages

setup(
    name="pyreachx",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ast2json>=0.3.0",
        "click>=7.0",
        "networkx>=2.5",
        "jinja2>=2.11.0",
        "PyYAML>=5.1.0",
    ],
    extras_require={
        'test': [
            'pytest>=6.0.0',
            'pytest-cov>=2.0.0',
            'pytest-mock>=3.0.0',
            'black>=21.0',
            'isort>=5.0.0',
            'mypy>=0.900',
            'flake8>=4.0.0',
            'flake8-bugbear>=21.0.0',
            'flake8-docstrings>=1.6.0',
            'flake8-import-order>=0.18.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'pyreachx=pyreachx.cli:main',
        ],
    },
    author="Aleksey Komissarov",
    author_email="ad3002@gmail.com",
    description="Python Code Reachability Analyzer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ad3002/pyreachx",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
)