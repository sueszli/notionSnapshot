import os
import subprocess


class DependencyManager:
    @staticmethod
    def _update_requirements() -> None:
        os.system("pip3 install pipreqs > /dev/null && rm -rf requirements.txt > /dev/null && pipreqs . > /dev/null")

    @staticmethod
    def run() -> None:
        if not os.name == "posix":
            print("quitting program: detected non unix system")
            exit(1)
        python_version = subprocess.run(["python3", "--version"], capture_output=True).stdout.decode("utf-8")
        if not python_version.startswith("Python 3"):
            print("quitting program: detected python version that is not 3")
            exit(1)

        os.system("python3 -m pip install --upgrade pip > /dev/null")

        # DependencyManager._update_requirements()
        os.system("pip3 install -r requirements.txt > /dev/null")
