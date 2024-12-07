from setuptools import setup, find_packages

setup(
    name='Cotizaciones',  # Nombre del paquete en PyPI
    version='0.1.0',  # Versión inicial del proyecto
    author='Nuria',
    author_email='nuria.zb1@gmail.com',
    description='Descripción corta de tu proyecto',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tu_usuario/tu_repositorio',  # URL del proyecto (opcional)
    packages=find_packages(),
    install_requires=[
        'krakenex',
        'matplotlib',
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versión mínima de Python requerida
)
