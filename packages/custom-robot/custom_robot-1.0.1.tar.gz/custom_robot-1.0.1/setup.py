from setuptools import setup, find_packages

setup(
    name='custom-robot',
    version='1.0.1',
    description='Customized version of the robot package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rishi Varma',
    author_email='rishi@criterionnetworks.com',
    license='GPL',
    packages=find_packages(),
    install_requires=[],  # List any dependencies here if needed
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
)

