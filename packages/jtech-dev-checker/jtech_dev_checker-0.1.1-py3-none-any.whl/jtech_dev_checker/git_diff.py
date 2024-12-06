import subprocess

def get_diff():
    try:
        result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        raise RuntimeError(f"Erro ao obter diff do Git: {e}")