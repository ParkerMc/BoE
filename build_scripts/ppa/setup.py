from setuptools import setup, find_packages

setup(
    name='boe',
    version='0.1',
	author='Nick R (ParkerMc)',
	author_email='',
    description='A chat platform that intends to look at other chat programs and take only the "Best of Everything".',
    packages=['boeClient'],
    package_data={'': ['LICENSE']},
    include_package_data=True,
    install_requires=[],
    scripts=['bin/boe'],
    data_files=[('share/icons/hicolor/scalable/apps', ['data/boe.svg']),('share/applications', ['data/BoE.desktop'])],
)
