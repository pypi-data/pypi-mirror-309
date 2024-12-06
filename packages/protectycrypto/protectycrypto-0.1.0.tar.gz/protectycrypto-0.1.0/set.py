from setuptools import setup, find_packages

setup(
    name='protectycrypto',  # Имя вашего пакета
    version='0.1.0',  # Версия пакета
    packages=find_packages(),  # Найдет все пакеты в проекте
    long_description=open('README.md').read(),  # Описание проекта
    long_description_content_type='text/markdown',
    author='u1kerq',
    author_email='ulkerqx1@gmail.com',
    url='https://github.com/u1kerqx1/protectycrypto',  # Ссылка на ваш репозиторий
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
