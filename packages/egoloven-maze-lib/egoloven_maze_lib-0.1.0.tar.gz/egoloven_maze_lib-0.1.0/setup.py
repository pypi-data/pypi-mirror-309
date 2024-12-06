from setuptools import setup, find_packages

setup(
    name='egoloven-maze-lib',
    version='0.1.0',
    description='Library for uni project.',
    author='egoloven',
    author_email='eugene.goloven@gmail.com',
    url='https://github.com/egoloven/egoloven-maze-lib.git',
    packages=find_packages(),  # This finds all the Python packages (directories with __init__.py)
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[],
    python_requires='>=3.6',
)

