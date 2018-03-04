from setuptools import setup

setup(name='nxdd',
    version='0.1',
    description='Networkx-backed decision diagrams',
    url='http://github.com/belarm/nxdd',
    author='belarm',
    # author_email='flyingcircus@example.com',
    license='MIT',
    packages=['nxdd'],
    install_requires=[
        'networkx',
    ],
    zip_safe=False)
