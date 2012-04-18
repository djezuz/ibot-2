from setuptools import setup, find_packages

setup(
    name='ibot',
    description='curse your way through itv net bot game',
    version='0.1',
    packages=find_packages(),
    install_requires=['requests'],
    author="Stephen M. McQuay",
    author_email="stephen@mcquay.me",
    url="http://github.com/smcquay/ibot",
    license="WTFPL",
    entry_points={
        'console_scripts': [
            'ibot = ibot.gui:main',
        ],
    },
)
