# mp_dev/commands/init_command.py
from ..project_generator import generate_project_structure


def run():
    print(f"Génération de l'architecture ...")
    generate_project_structure()
    print("Architecture de projet générée avec succès.")
