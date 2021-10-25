import os
from re import sub
import sys
import subprocess
import shutil

from rich.console import Console

console = Console()

# TODOs ------------------------------------------------------------------------------------------------
# todo - add an else block to if blocks where you check the return code of processes

def get_project_name():
    # TODO - Split using _
    project_name = input("What is the name of the project? ")
    project_name = "".join(project_name.split(" "))
    return project_name

def create_dir_for_project(project_name):
    try:
        os.makedirs(project_name)
    except FileExistsError as e:
        # TODO -  If the directory exists, ask the user whether you should remove it and set up the project anew
        console.log("[bold red]The directory already exists[/bold red]")
        console.log(e)

def get_virtual_env_to_use():
    console.print()
    console.print("[bold magenta]Choose virtual environment package to use[/bold magenta]")
    console.print("1 -> [yellow]pipenv[/yellow]")
    console.print("2 -> [yellow]venv[/yellow]")
    while True:
        try:
            virtual_env = int(input("Select virtual env to use by number: "))
            if virtual_env in [1, 2]:
                break
            else:
                raise ValueError
        except ValueError as e:
            console.log("[bold red]Enter integer value 1 or 2 only[/bold red]")
            continue
    return virtual_env

def install_pipenv():
    try:
        import pipenv
        console.print("[bold green]pipenv detected...[/bold green]")
        console.print()
    except ModuleNotFoundError as e:
        console.log("[bold red]pipenv is not installed. pipenv will be installed on your system.[/bold red]")
        install_process = subprocess.run('pip install pipenv', shell=True)
        if install_process.returncode == 0:
            console.print("[bold green]pipenv was installed successfully!!![/bold green]")
            console.print()

def create_virtualenv_with_pipenv(project_name):
    while True:
        try:
            console.print("[yellow bold]Please ensure that the version you are using is installed on your device[/yellow bold]")
            python_version = float(input("Enter the python version to use, e.g: 3.8: ")) # TODO add note to use only installed python versions
            create_virtualenv_process = subprocess.run(f'pipenv --python {python_version}', shell=True)
            if create_virtualenv_process.returncode == 0:
                success_msg = f"virtual environment created successfully in the [red]{project_name}[/red] directory."
                console.print(f"[bold green]{success_msg}[/bold green]")
                console.print()
            break
        except ValueError:
            console.log("The python version should be a float value.")
            continue

def query_user_for_drf_install_option():
    while True:
        try:
            install_drf = int(input("Will you use django REST framework in your project? ( 1 - yes, 0 - no): "))
            if install_drf in [0, 1]:
                break
            else:
                raise ValueError
        except ValueError:
            console.log("Enter integer 1 or 0 only")
            continue
    return install_drf

def install_packages_in_pipenv_virtualenv():
    install_drf = query_user_for_drf_install_option()    
    packages = 'django pytest-django psycopg2-binary pytest-cov django-extensions pytest-factoryboy werkzeug ipython pytest-factoryboy pytest-xdist pillow'
    if install_drf == 1:
        packages = packages + ' ' + 'djangorestframework markdown django-filter'
    install_required_packages_process = subprocess.run(f'pipenv install {packages}', shell=True)
    if install_required_packages_process.returncode == 0:
        console.print("[bold green]Installation of packages successfull!!![/bold green]")
        console.print("[bold magenta]These packages were installed[/bold magenta]")
        console.print()
    return install_required_packages_process.returncode

def create_django_project(project_name):
    console.print("[bold yellow]creating django project ...[/bold yellow]")
    create_django_project_process = subprocess.run(f'pipenv run django-admin startproject {project_name.upper()} .', shell=True)
    if create_django_project_process.returncode == 0:
        console.print("[bold green]django project created successfully !!![/bold green]")
        console.print()

def create_config_folders_and_files(project_folder):
    console.print("[bold yellow]creating config folders and settings files ...[/bold yellow]")
     # create config and settings folder
    os.makedirs('config/settings/')
    # create init files
    init_file_name = '__init__.py'
    try:
        with open(os.path.join(project_folder, 'config', init_file_name), 'w') as file1, \
            open(os.path.join(project_folder, 'config/settings', init_file_name), 'w') as file2:
            pass
    except FileExistsError as e:
        console.log(e)

    # create 3 files under the config file
    try:
        with open(os.path.join(project_folder, 'config', 'asgi.py'), 'w') as file1, \
            open(os.path.join(project_folder, 'config', 'wsgi.py'), 'w') as file2, \
            open(os.path.join(project_folder, 'config', 'urls.py'), 'w') as file3:
            pass
    except FileExistsError as e:
        console.log(e)
    
    # create four empty settings files under the settings directory
    try:
        with open(os.path.join(project_folder, 'config/settings', 'development.py'), 'w') as devfile, \
            open(os.path.join(project_folder, 'config/settings', 'production.py'), 'w') as prodfile, \
            open(os.path.join(project_folder, 'config/settings', 'testing.py'), 'w') as testfile, \
            open(os.path.join(project_folder, 'config/settings', 'base.py'), 'w') as basefile:
            pass
    except FileExistsError as e:
        console.log(e)
    console.print("[bold green]successfully created config folders and settings files !!![/bold green]")
    console.print()


def main():
    # TODO - detect the operating system so as to know what commands to use
    
    console.print()
    console.print("[bold blue]Django Project Setup[/bold blue]")
    # Get the project name
    project_name = get_project_name()
    # Create a directory for the project name
    create_dir_for_project(project_name)
    
    os.chdir(project_name) # Change the direcotry to the project directory
    project_root_folder = os.getcwd() # This is the folder containing the project

    # Ask the user which virtual environment they would like to use
    virtual_env = get_virtual_env_to_use()
        
    # Logic to create an activate virtual environment virtual_env is 1
    if virtual_env == 1:
        try:
            import pip
            install_pipenv() # install pipenv if it doesn't exist

            # create a virtualenvironment usingn pipenv in this directory
            # create_virtualenv_with_pipenv(project_name) # ! uncomment this

            # TODO - create django project in the project folder directory
            # todo - install the required packages
            
            # TODO - ask the user to provide the version numbers of the packages, leave it blank to install the latest packages
            # TODO - ask the user for which database they will be using and configure the system accordingly
            # package_install_status = install_packages_in_pipenv_virtualenv() # ! uncomment this

            package_install_status = 0
            if package_install_status == 0:
                # todo - create the django project in the project folder 
                create_django_project(project_name) # ! uncomment this
                # todo - create the config files and folders
                project_name = project_name.upper() # project name is now upper case
                os.chdir(project_name)
                project_folder = os.getcwd()
                create_config_folders_and_files(project_folder) # create the config folders and files
                # todo - move the default config files to the config directory i.e urls.py, wsgi.py, asgi.py
                # move the default config files to the config folder
                config_dir = os.path.join(project_folder, 'config')
                files = ['urls.py', 'asgi.py', 'wsgi.py'] # the filenames to handle the copy for
                for file in files:
                    shutil.move(os.path.join(project_folder, file), os.path.join(config_dir, file))

                # copy the content of the settings file to the base.py file
                settings_dir = os.path.join(config_dir, 'settings')
                with open(os.path.join(project_folder, 'settings.py'), 'r') as file1, \
                    open(os.path.join(settings_dir, 'base.py'), 'w') as file2:
                    # read each line in file 1
                    for line in file1:
                        file2.write(line)


                # todo - create a custom user 
                # todo - add configuration of the packages that need it

            

        except ModuleNotFoundError as e:
            # TODO - if pip is not installed systemwide, ask user if pip should be installed
            console.log("[bold red]pip is not installed. Please install pip on your system.[/bold red]")

        
        
    # TODO Logic to create an environment using venv


if __name__ == "__main__":
    main()
