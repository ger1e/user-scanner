import subprocess
import sys
from colorama import Fore


def get_version(package_name):
    try:
        from importlib.metadata import version  # Python 3.8+
        return version(package_name)
    except Exception:
        return "Unknown"


def update_self() -> bool:
    print("Updating user-scanner using pip...\n")
    try:
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "user-scanner",
        ])
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Failed to update user-scanner: {e}{Fore.RESET}")
        return False

    user_scanner_ver = get_version("user-scanner")
    print("\nInstalled Version:")
    print(f"   • user-scanner: {user_scanner_ver}")
    return True


if __name__ == "__main__":
    user_scanner_ver = get_version("user-scanner")
    print(user_scanner_ver)
