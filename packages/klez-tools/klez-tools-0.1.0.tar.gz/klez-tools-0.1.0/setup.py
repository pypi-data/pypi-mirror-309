from setuptools import setup, find_packages

setup(
    name="klez-tools",
    version="0.1.0",
    description="A simple tool to encode names using numeric cryptography logic.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Joseph Klez",
    author_email="klez@cock.li",
    url="https://ammo.lol/Klez",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=[
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "klez-tools=klez_tools.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
