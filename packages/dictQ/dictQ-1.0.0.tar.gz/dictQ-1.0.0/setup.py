from setuptools import setup, find_packages

setup(
    name="dictQ",
    version="1.0.0",
    author="khiat Mohammed Abderrezzak",
    author_email="khiat.dev@gmail.com",
    license="MIT",
    description="Sophisticate Searching Algorithms",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/dictQ/",
    packages=find_packages(),
    install_requires=[
        "pynput>=1.7.7",
        "pyfiglet>=1.0.2",
        "hashtbl>=1.0.5",
    ],
    keywords=[
        "sorting algorithms",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
