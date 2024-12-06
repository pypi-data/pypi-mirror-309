from setuptools import setup, find_packages
setup(
name='journey_orchestrate',
version='0.0.1',
author='Dhivya Nagasubramanian',
author_email='nagas021@alumni.umn.edu',
description='For a customer journey involving multiple marketing channels through which messages were delivered, we can orchestrate and stitch together the individual journey paths for each customer, providing a cohesive view of their interactions across all touchpoints.',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)