from setuptools import setup, find_packages

setup(
    name="manipulador_pdf",
    version="0.0.6",
    description="Uma biblioteca para manipulação de arquivos .pdf.",
    author="Luiz Gustavo Queiroz",
    author_email="luizgusqueiroz@gmail.com",
    packages=find_packages(),  # Isso encontra e inclui automaticamente os pacotes (pastas com __init__.py)
    install_requires=[],  # Dependências, se houver
)
