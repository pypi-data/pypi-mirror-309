from .templates import (config_template, connection_template, data_base_session_middleware_template, gitignore_template,
                        is_authenticated_middleware_template, main_template, migration_template, token_schema_template,
                        user_controller_template, user_model_template, dockerfile_template, docker_compose_template)
import os


def generate_project_structure(project_name):
    project_structure = {
        "README.txt": "Ceci est le fichier README pour votre projet.\n\n### Description du Projet\nExpliquez ici les objectifs et le fonctionnement de votre projet.",
        "app": {
            "__init__.py": "",
            "Controller": {
                "__init__.py": "",
                "UserController.py": user_controller_template.get_content(),
            },
            "DB": {
                "__init__.py": "",
                "Connection.py": connection_template.get_content(),
                "Migration.py": migration_template.get_content(),
                "Model": {
                    "__init__.py": "",
                    "UserModel.py": user_model_template.get_content(),
                },
            },
            "Middleware": {
                "__init__.py": "",
                "DatabaseSessionMiddleware.py": data_base_session_middleware_template.get_content(),
                "IsAuthenticatedMiddleware.py": is_authenticated_middleware_template.get_content(),
            },
            "Router": {
                "__init__.py": ""
            },
            "Schema": {
                "__init__.py": "",
                "TokenSchema.py": token_schema_template.get_content(),
            },
        },
        "core": {
            "config.py": config_template.get_content(project_name),
        },
        ".gitignore": gitignore_template.get_content(),
        "Dockerfile": dockerfile_template.get_content(),
        "docker-compose.yml": docker_compose_template.get_content(),
        "main.py": main_template.get_content()
    }

    def create_structure(base_path, structure):
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(path, content)
            else:
                with open(path, "w") as f:
                    f.write(content)

    create_structure(".", project_structure)
    print("Architecture de base du projet générée avec succès.")