from setuptools import setup, find_packages

setup(
    name='klez-tools',
    version='0.1.2',
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'klez-tools=klez_tools.main:main',
        ],
    },
    install_requires=[
        'rich',
    ],
    author="Joseph Klez",
    author_email="klez@cock.li",
    description="A set of tools for encoding names in a unique format.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://ammo.lol/Klez',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
