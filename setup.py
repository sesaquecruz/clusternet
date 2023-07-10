from setuptools import setup, find_packages

setup(
    name='clusternet',
    version='0.8.2',
    description='Distributed Software Defined Network Emulation',
    long_description='Distributed Software Defined Network Emulation',
    keywords=['networking', 'emulator', 'containernet', 'mininet', 'OpenFlow', 'SDN', 'fog'],
    url='https://github.com/EsauM10/clusternet',
    author='Esaú Mascarenhas',
    author_email='esaumasc@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python 3.8',
        'Topic :: System :: Emulators'
        'Operating System :: Ubunbu OS'
    ],
    packages=find_packages(),
    install_requires = [
        'Flask',
        'Flask-Cors',
        'httpx'
    ],
    entry_points={
        'console_scripts': [
            'RunWorker = clusternet.server.worker_app:main',
        ]
    },
    include_package_data=True,
    zip_safe=False
)