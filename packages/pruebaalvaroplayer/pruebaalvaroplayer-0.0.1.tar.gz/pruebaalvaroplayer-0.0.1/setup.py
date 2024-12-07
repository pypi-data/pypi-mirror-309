import setuptools
from pathlib import Path

long_desc = Path("README.md").read_text()

setuptools.setup(
    name="pruebaalvaroplayer",  # nombre del paquete que tendrá en pypi
    version="0.0.1",  # versión del paquete
    long_description=long_desc,  # descripción del paquete importado de README.md
    packages=setuptools.find_packages(  # indicar donde se encuentran los paquetes
        exclude=["mocks", "tests"]  # excluir carpetas
    )
)

# python3 setup.py sdist bdist_wheel -> generar 'dist' y 'build'
# en dist hay un .tar.gz
# twine upload dist/* -> subir paquete al pypi, pedirá usuario y contraseña o api token
