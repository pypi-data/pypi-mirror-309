# mp_dev/commands/init_command.py
from ..project_generator import generate_project_structure


def run():
    project_name = input("Nom du projet: ")
    print(f"Génération de l'architecture ...")
    generate_project_structure(project_name)
    print("Architecture de projet générée avec succès.")
