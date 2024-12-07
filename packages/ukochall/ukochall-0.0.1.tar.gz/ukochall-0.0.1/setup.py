from setuptools import setup, find_packages

setup(
    name='ukochall',
    version='0.0.1',
    description='testuko',
    author='uko',
    author_email='cora9448@naver.com',
    url='',
    install_requires=['os'],
    packages=find_packages(exclude=[]),
    keywords=['ukodreamhack'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)