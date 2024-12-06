from setuptools import setup, find_packages

setup(
    name="manipulador_pdf",
    version="0.0.8",
    description="Uma biblioteca para manipulação de arquivos .pdf.",
    author="Luiz Gustavo Queiroz",
    author_email="luizgusqueiroz@gmail.com",
    packages=find_packages(),  # Isso encontra e inclui automaticamente os pacotes (pastas com __init__.py)
    install_requires=[
        "google-auth",
        "google-auth-oauthlib",
        "google-api-python-client",
        "PyPDF2",
        "pytesseract",
        "opencv-python",
        "PyMuPDF",
        "pandas",
        "Pillow",
        "tqdm",
    ],
)
