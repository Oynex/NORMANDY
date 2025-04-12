from setuptools import setup, find_packages

setup(
    name="normandy",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pygame",
    ],
    package_data={
        "": ["images/*.bmp"],
    },
    entry_points={
        "console_scripts": [
            "normandy=normandy:rundagame",
        ],
    },
)
