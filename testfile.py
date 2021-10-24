from app import console


packages = 'django pytest-django pytest-cov django-extensions pytest-factoryboy werkzeug ipython'

for package in packages.split():
    console.print(f"[yellow]{package}[yellow]")