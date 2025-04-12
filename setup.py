from setuptools import setup, find_packages

setup(
    name='Normandy',
    version='1.0.0', 
    description='Shoot em Reapers',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pygame',
    ],
    entry_points={
        'console_scripts': [
            'normandy=normandy:rundagame',
        ]
    },
    package_data={
        '': ['images/*'],
    },
)
