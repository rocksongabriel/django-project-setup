import os
import sys
import subprocess

from rich.console import Console

console = Console()

def get_project_name():
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


def main():
    # TODO - detect the operating system so as to know what commands to use
    
    console.print()
    console.print("[bold blue]Django Project Setup[/bold blue]")
    # Get the project name
    project_name = get_project_name()
    # Create a directory for the project name
    create_dir_for_project(project_name)
    
    os.chdir(project_name) # Change the direcotry to the project directory
    project_directory = os.getcwd()

    # Ask the user which virtual environment they would like to use
    virtual_env = get_virtual_env_to_use()
        
    # Logic to create an activate virtual environment virtual_env is 1
    if virtual_env == 1:
        try:
            import pip
            install_pipenv() # install pipenv if it doesn't exist
            # create a virtualenvironment usingn pipenv in this directory
  
            while True:
                try:
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

        except ModuleNotFoundError as e:
            # TODO - if pip is not installed systemwide, ask user if pip should be installed
            console.log("[bold red]pip is not installed. Please install pip on your system.[/bold red]")

        
        
    # TODO Logic to create an environment using venv


if __name__ == "__main__":
    main()
