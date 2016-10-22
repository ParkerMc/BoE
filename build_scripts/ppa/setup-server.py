from setuptools import setup, find_packages

setup(
    name='boe-server',
    version='0.1.1',
	author='Nick R (ParkerMc)',
	author_email='',
    description='A chat platform that intends to look at other chat programs and take only the "Best of Everything".',
    packages=['boeServer'],
    package_data={'': ['LICENSE']},
    include_package_data=True,
    install_requires=[],
    scripts=['bin/boe-server'],
)
