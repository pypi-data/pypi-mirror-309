from setuptools import setup, find_packages
setup(
    name="Stormy_Seas_package",
    version="0.9",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pygame",
    ],
    entry_points={
        'console_scripts': [
            'Stormy_Seas_package = Stormy_Seas_package.__main__:main'
        ]
    },
    package_data={
        '': ['Stormy_Seas_package/assets/*'],
    },
)