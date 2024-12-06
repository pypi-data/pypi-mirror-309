from setuptools import setup, find_packages

setup(
    name='prlps_websearch',
    version='0.0.1b',
    author='prolapser',
    packages=find_packages(),
    url='https://github.com/prolapser/prlps_websearch',
    license='LICENSE.txt',
    description='веб поиск',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.10',
    install_requires=['httpx', 'parsel'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
