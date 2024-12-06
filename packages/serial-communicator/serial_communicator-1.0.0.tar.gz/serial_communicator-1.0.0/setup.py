from setuptools import setup, find_packages

setup(
    name='serial_communicator',
    version='1.0.0',
    author='Oleg Kravtsov',
    author_email='kravtsov.oleg@vk.com',
    description='Модуль для взаимодействия с устройствами через последовательный порт.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RadioPizza/serial_communicator',
    license='MIT',
    packages=find_packages(exclude=('tests', 'examples')),
    py_modules=['serial_communicator'],
    install_requires=['pyserial'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
