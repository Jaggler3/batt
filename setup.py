from setuptools import setup
setup(
    name='bos-daemon',
    version='0.1.0',
    packages=['bos-daemon'],
    install_requires=[
		'psutil',
    ],
    entry_points={
        'console_scripts': [
            'bos-daemon = bos-daemon.__main__:main'
        ]
    }
)
