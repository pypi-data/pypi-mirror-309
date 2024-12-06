from setuptools import setup, find_packages

setup(
    name='genetic-algorithm-py',  # Replace with your package name
    version='1.0.1',
    description='A genetic algorithm library for solving optimization problems',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kanzariya Hardik',
    author_email='hardikkanzariya091@gmail.com',
    url='https://github.com/MrHardik-k/genetic-algorithm',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[],
)
