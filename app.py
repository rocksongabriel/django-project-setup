import os
from re import sub
import sys
import subprocess
import shutil

from rich.console import Console

from utils import secret_key

console = Console()

root_of_this_code = os.getcwd()

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
        console.print()
    return install_required_packages_process.returncode, install_drf

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

def write_settings_to_dev_prod_test(project_folder):
    settings_files_py = ['development.py', 'production.py', 'testing.py']
    settings_files_txt = ['development_settings.txt', 'production_settings.txt', 'testing_settings.txt']

    for index,setting_file_py in enumerate(settings_files_py):
        setting_file_py_path = os.path.join(project_folder, 'config', 'settings', '{}'.format(setting_file_py))
        setting_file_txt = settings_files_txt[index]
        setting_file_txt_path = os.path.join(root_of_this_code, 'files', '{}'.format(setting_file_txt))

        # read settings from txt file
        with open(setting_file_txt_path) as file1:
            lines_to_write = file1.readlines()

        # write settings to py file
        with open(setting_file_py_path, 'w') as file2:
            file2.writelines(lines_to_write)

        # modify the secret key line
        with open(setting_file_py_path) as file1:
            old_secret_key_line = "SECRET_KEY = ''"
            new_secret_key_line = "SECRET_KEY = '{}'".format(secret_key())
            new_setting_file = file1.read().replace(old_secret_key_line, new_secret_key_line)
        
        with open(setting_file_py_path, 'w') as file2:
            file2.writelines(new_setting_file)

def change_base_dir_urlconf_wsgi_app_setting(base_settings_file, project_name):
    old_base_dir = 'BASE_DIR = Path(__file__).resolve().parent.parent'
    new_base_dir = 'BASE_DIR = Path(__file__).resolve().parent.parent.parent'
    old_url_conf = "ROOT_URLCONF = '{}.urls'".format(project_name)
    new_url_conf = "ROOT_URLCONF = '{}.config.urls'".format(project_name)
    old_wsgi_application = "WSGI_APPLICATION = '{}.wsgi.application'".format(project_name)
    new_wsgi_application = "WSGI_APPLICATION = 'TESTPROJECT.config.wsgi.application'".format(project_name)
    with open(base_settings_file, 'r') as file:
        newBase = file.read().replace(old_base_dir, new_base_dir)
        newBase = newBase.replace(old_url_conf, new_url_conf)
        newBase = newBase.replace(old_wsgi_application, new_wsgi_application)
    
    with open(base_settings_file, 'w') as file:
        file.write(newBase)

def delete_common_settings_from_base_settings(base_settings_file):
    lines = []
    lines_to_delete = []

    with open(base_settings_file, 'r') as file:
        lines = file.readlines()
        for the_line in lines:
            if the_line.startswith('# Quick-start'):
                lines_to_delete.append(the_line)
            elif the_line.startswith('SECRET_KEY'):
                lines_to_delete.append(the_line)
            elif the_line.startswith('# SECURITY WARNING:'):
                lines_to_delete.append(the_line)  
            elif the_line.startswith('# See ht'):
                lines_to_delete.append(the_line)
            elif the_line.startswith('DEBUG'):
                lines_to_delete.append(the_line)
            elif the_line.startswith('ALLOWED_HOSTS'):
                lines_to_delete.append(the_line)

    with open(base_settings_file, 'w') as file:
        for line in lines:
            if line not in lines_to_delete:
                file.write(line)

    new_base_file_lines = []
    with open(base_settings_file, 'r') as file:
        new_base_file_lines = file.readlines()

    lines_to_write_to_base_file = new_base_file_lines[0:18] + new_base_file_lines[23:] # remove the blank lines between the BASE_DIR line and the INTALLED_APPS line
    with open(base_settings_file, 'w') as file:
        file.writelines(lines_to_write_to_base_file)

def delete_database_settings_from_base_settings(base_settings_file):
    
    with open(os.path.join(root_of_this_code, 'files', 'old_database_setting.txt')) as file:
        findlines = file.readlines()

    with open (base_settings_file, 'r') as file:
        lines = file.readlines()

    with open(base_settings_file, 'w') as file:
        for line in lines:
            if line not in findlines:
                file.write(line)

    new_base_file_lines = []
    with open(base_settings_file, 'r') as file:
        new_base_file_lines = file.readlines()

    lines_to_write_to_base_file = new_base_file_lines[0:59] + new_base_file_lines[64:] # remove the blank lines between the WSGI_APPLICATION and # Password validation
    with open(base_settings_file, 'w') as file:
        file.writelines(lines_to_write_to_base_file)

def add_extra_apps_to_installed_apps(base_settings_file):
    with open(base_settings_file, 'r') as file:
        lines = file.readlines()
    lines_to_write = lines[:19] + lines[29:]

    with open(base_settings_file, 'w') as file:
        for line in lines_to_write:
            file.write(line) 

    # write the new application settings
    with open(base_settings_file, 'r') as file:
        newBase = []
        for line in file.readlines():
            if line.startswith('# Application definition'):
                with open(os.path.join(root_of_this_code, 'files', 'installed_apps_settings_drf.txt')) as file:
                    newBase.append(line)
                    for line in file.readlines():
                        newBase.append(line)
            else:
                newBase.append(line)

    with open(base_settings_file, 'w') as file:
        file.writelines(newBase)

def add_media_settings_url_to_urls(config_dir):
    base_url_file = os.path.join(config_dir, 'urls.py')
    with open(base_url_file, 'a') as file1:
        with open(os.path.join(root_of_this_code, 'files', 'media_settings_in_urls.txt')) as file2:
            for line in file2:
                file1.write(line)

def add_static_files_and_media_settings(base_settings_file, config_dir):
    with open(base_settings_file) as file:
        lines = file.readlines()

    with open(base_settings_file, 'r') as file:
        newBase = []
        for line in lines:
            if line.startswith('STATIC_URL'):
                newBase.append("MEDIA_URL = '/media/'\n")
                newBase.append("MEDIA_ROOT = BASE_DIR / 'media'\n\n")

                newBase.append("STATIC_ROOT = BASE_DIR / 'staticfiles'\n")
                newBase.append("STATICFILES_DIRS = [\n\tBASE_DIR / 'static',\n]\n")
            if line.endswith("'DIRS': [],\n"):
                newBase.append("\t\t'DIRS': [BASE_DIR / 'templates',],\n")
            else:
                newBase.append(line)

    with open(base_settings_file, 'w') as file:
        file.writelines(newBase)

    add_media_settings_url_to_urls(config_dir)

def modify_manage_file_to_use_development_settings(project_root_folder, project_name):
    manage_file = os.path.join(project_root_folder, 'manage.py')
    with open(manage_file) as file:
        old_line = "os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{}.settings'".format(project_name)
        new_line = "os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{}.config.settings.development'".format(project_name)
        newManageFile = file.read().replace(old_line, new_line)

    with open(manage_file, 'w') as file:
        file.writelines(newManageFile)

def modify_asgi_and_wsgi_files_to_use_the_production_settings(config_dir):
    files = ['asgi.py', 'wsgi.py']
    for file_name in files:
        file_path = os.path.join(config_dir, file_name)
        with open(file_path) as file:
            old_line = "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TESTPROJECT.settings'"
            new_line = "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TESTPROJECT.config.settings.production'"
            newFile = file.read().replace(old_line, new_line)

        with open(file_path, 'w') as file:
            file.writelines(newFile)

def write_django_rest_framework_url_to_urls_py(config_dir):
    url_file_path = os.path.join(config_dir, 'urls.py')
    with open(url_file_path) as file:
        file1 = file.read().replace('from django.urls import path', 'from django.urls import path, include')
        new_line = "path('api-auth/', include('rest_framework.urls'))"
        file2 = file1.replace(']', '\t{}\n]'.format(new_line))

    with open(url_file_path, 'w') as file:
        file.writelines(file2)

def add_custom_user_model(project_root_folder, base_settings_file):
    os.chdir(project_root_folder)
    create_users_app_process = subprocess.run('pipenv run python manage.py startapp users', shell=True)
    # add new Users definition to the models.py
    models_file = os.path.join(project_root_folder, "users", "models.py")
    user_model_code_txt = os.path.join(root_of_this_code, "files", "user_model_code.txt")
    with open(user_model_code_txt) as file1:
        lines_to_write = file1.readlines()
    
    with open(models_file, 'w') as file:
        file.writelines(lines_to_write)

    # Add the custom user to the settings file
    with open(base_settings_file, 'a') as file:
        file.write("\nAUTH_USER_MODEL = 'users.User'\n")

    # Add the users app to the installed_apps 
    with open(base_settings_file) as file1:
        lines_to_write = "\t'django.contrib.staticfiles',\n\n\t# Developer's apps\n\t'users.apps.UsersConfig'\n"
        lines = file1.read().replace("    'django.contrib.staticfiles',\n", lines_to_write)

    with open(base_settings_file, 'w') as file2:
        file2.writelines(lines)



def main():
    # TODO - detect the operating system so as to know what commands to use
    
    console.print()
    console.print("[bold blue]Django Project Setup[/bold blue]")
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

            # create_virtualenv_with_pipenv(project_name) # ! uncomment this

            # TODO - ask the user to provide the version numbers of the packages, leave it blank to install the latest packages
            # TODO - ask the user for which database they will be using and configure the system accordingly
            # package_install_status, installed_drf = install_packages_in_pipenv_virtualenv() # ! uncomment this

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

                # copy the content of the settings.py file to the base.py file
                settings_dir = os.path.join(config_dir, 'settings')
                shutil.move(os.path.join(project_folder, 'settings.py'), os.path.join(settings_dir, 'base.py'))
                
                # todo - edit the base.py file
                base_settings_file = os.path.join(settings_dir, 'base.py')

                # Change where the BASE_DIR is pointing and change the root conf, and wsgi application settings
                change_base_dir_urlconf_wsgi_app_setting(base_settings_file, project_name)

                delete_common_settings_from_base_settings(base_settings_file)

                write_settings_to_dev_prod_test(project_folder)
                delete_database_settings_from_base_settings(base_settings_file)

                # if installed_drf == 1: # ! uncomment this
                #     add_extra_apps_to_installed_apps(base_settings_file)
                #     write_django_rest_framework_url_to_urls_py(config_dir)

                add_static_files_and_media_settings(base_settings_file, config_dir)
                modify_manage_file_to_use_development_settings(project_root_folder, project_name)
                modify_asgi_and_wsgi_files_to_use_the_production_settings(config_dir)

                # create a custom user 
                add_custom_user_model(project_root_folder, base_settings_file)
                
                # todo - add configuration of the packages that need it

        except ModuleNotFoundError as e:
            # TODO - if pip is not installed systemwide, ask user if pip should be installed
            console.log("[bold red]pip is not installed. Please install pip on your system.[/bold red]")
    # TODO Logic to create an environment using venv

if __name__ == "__main__":
    main()
