from setuptools import setup, find_packages

from prlps_websearch.utils import PKG_NAME, VERSION

setup(
    name=PKG_NAME,
    version=VERSION,
    author='prolapser',
    packages=find_packages(),
    url='https://github.com/prolapser/prlps_websearch',
    license='LICENSE.txt',
    description='веб поиск',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.10',
    install_requires=['httpx', 'parsel', 'nest_asyncio', 'packaging', 'prlps_fakeua'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
