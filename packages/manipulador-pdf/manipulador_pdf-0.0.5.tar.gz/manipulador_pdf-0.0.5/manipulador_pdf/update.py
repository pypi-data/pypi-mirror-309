import importlib.metadata
import subprocess
import socket


def update():
    """
    Atualiza (ou instala) a biblioteca istalada para a versão mais recente.

    """
    pacote = "manipulador_pdf"
    # Verifica se há conexão para o download dos arquivos.
    if tem_conexao():
        try:
            # Verifica se o pacote está instalado.
            importlib.metadata.version(pacote)
            print("Verificando atualizações...")
            # Atualiza a biblioteca.
            subprocess.check_call([subprocess.sys.executable, "-m", "pip", "install", "--upgrade", pacote])
        except importlib.metadata.PackageNotFoundError:
            print("Instalando recursos...")
            # Instala a biblioteca.
            subprocess.check_call([subprocess.sys.executable, "-m", "pip", "install", pacote])


def tem_conexao() -> bool:
    try:
        # Estabelece conexão com o servidor DNS do Google.
        socket.create_connection(('8.8.8.8', 53), timeout=5)
        return True
    except Exception:
        return False
