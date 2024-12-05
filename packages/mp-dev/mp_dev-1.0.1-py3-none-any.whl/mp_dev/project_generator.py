import os


def generate_project_structure():
    template_dir = "./templates"
    templates = [
        "config_template.py",
        "gitignore_template.py",
        "main_template.py",
        "data_base_session_middleware_template.py",
        "token_schema_template.py",
        "user_model_template.py",
        "user_controller_template.py",
        "is_authenticated_middleware_template.py",
        "migration_template.py",
        "connection_template.py"
    ]

    template_contents = {}
    for template in templates:
        with open(os.path.join(template_dir, template), "r") as f:
            template_contents[template] = f.read()

    project_structure = {
        "README.txt": "Ceci est le fichier README pour votre projet.\n\n### Description du Projet\nExpliquez ici les objectifs et le fonctionnement de votre projet.",
        "app": {
            "__init__.py": "",
            "Controller": {
                "__init__.py": "",
                "UserController.py": template_contents["user_controller_template.py"],
            },
            "DB": {
                "__init__.py": "",
                "Connection.py": template_contents["connection_template.py"],
                "Migration.py": template_contents["migration_template.py"],
                "Model": {
                    "__init__.py": "",
                    "UserModel.py": template_contents["user_model_template.py"],
                },
            },
            "Middleware": {
                "__init__.py": "",
                "DatabaseSessionMiddleware.py": template_contents["data_base_session_middleware_template.py"],
                "IsAuthenticatedMiddleware.py": template_contents["is_authenticated_middleware_template.py"],
            },
            "Router": {
                "__init__.py": ""
            },
            "Schema": {
                "__init__.py": "",
                "TokenSchema.py": template_contents["token_schema_template.py"],
            },
        },
        "core": {
            "config.py": template_contents["config_template.py"],
        },
        ".gitignore": template_contents["gitignore_template.py"],
        "main.py": template_contents["main_template.py"]
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