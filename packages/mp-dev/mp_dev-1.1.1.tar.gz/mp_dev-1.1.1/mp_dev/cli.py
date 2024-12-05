# mp_dev/cli.py
import sys
from .commands import init_command, help_command


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "help"
    if command == "init":
        init_command.run()
    elif command == "help":
        help_command.run()
    else:
        print(f"Commande '{command}' non reconnue. Utilisez 'mp-dev help' pour la liste des commandes disponibles.")
