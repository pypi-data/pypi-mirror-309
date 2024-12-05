# mp_dev/project_generator.py
import os


def generate_project_structure():
    # Charger le contenu de chaque fichier template
    with open("mp_dev/templates/config_template.py", "r") as f:
        config_content = f.read()
    with open("mp_dev/templates/gitignore_template.py", "r") as f:
        gitignore_content = f.read()
    with open("mp_dev/templates/main_template.py", "r") as f:
        main_content = f.read()
    with open("mp_dev/templates/data_base_session_middleware_template.py", "r") as f:
        data_base_session_middleware_content = f.read()
    with open("mp_dev/templates/token_schema_template.py", "r") as f:
        token_schema_content = f.read()
    with open("mp_dev/templates/user_model_template.py", "r") as f:
        user_model_content = f.read()
    with open("mp_dev/templates/user_controller_template.py", "r") as f:
        user_controller_content = f.read()
    with open("mp_dev/templates/is_authenticated_middleware_template.py", "r") as f:
        is_authenticated_middleware_content = f.read()
    with open("mp_dev/templates/migration_template.py", "r") as f:
        migration_content = f.read()
    with open("mp_dev/templates/connection_template.py", "r") as f:
        connection_content = f.read()

    # Définir la structure de projet, avec du contenu par défaut pour certains fichiers
    project_structure = {
        "README.txt": "Ceci est le fichier README pour votre projet.\n\n### Description du Projet\nExpliquez ici les objectifs et le fonctionnement de votre projet.",
        "app": {
            "__init__.py": "",
            "Controller": {
                "__init__.py": "",
                "UserController.py": user_controller_content,
            },
            "DB": {
                "__init__.py": "",
                "Connection.py": connection_content,
                "Migration.py": migration_content,
                "Model": {
                    "__init__.py": "",
                    "UserModel.py": user_model_content,
                },
            },
            "Middleware": {
                "__init__.py": "",
                "DatabaseSessionMiddleware.py": data_base_session_middleware_content,
                "IsAuthenticatedMiddleware.py": is_authenticated_middleware_content,
            },
            "Router": {
                "__init__.py": ""
            },
            "Schema": {
                "__init__.py": "",
                "TokenSchema.py": token_schema_content,
            },
        },
        "core": {
            "config.py": config_content,
        },
        ".gitignore": gitignore_content,
        "main.py": main_content
    }

    # Fonction récursive pour créer des dossiers et fichiers
    def create_structure(base_path, structure):
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(path, content)
            else:
                with open(path, "w") as f:
                    f.write(content)

    # Générer la structure de projet
    create_structure(".", project_structure)
    print("Architecture de base du projet générée avec succès.")
