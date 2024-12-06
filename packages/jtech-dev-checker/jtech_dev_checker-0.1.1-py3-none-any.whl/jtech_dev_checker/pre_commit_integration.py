import os
import shutil


def install_pre_commit_hook():
    """Instala o hook pre-commit no repositório Git local."""
    git_hooks_dir = os.path.join(".git", "hooks")
    pre_commit_hook = os.path.join(os.path.dirname(__file__), "../hook/pre-commit")

    if not os.path.isdir(git_hooks_dir):
        raise FileNotFoundError("Este repositório não possui um diretório .git/hooks. Confirme se está dentro de um repositório Git.")

    shutil.copy(pre_commit_hook, os.path.join(git_hooks_dir, "pre-commit"))
    os.chmod(os.path.join(git_hooks_dir, "pre-commit"), 0o755)
    print("Hook pre-commit instalado com sucesso!")


def main():
    print("Instalando o JTech Dev Checker...")
    install_pre_commit_hook()
