import subprocess
import pyflatpak

class manager():

    def __init__(self, remote_name="flathub", remote_url="https://dl.flathub.org/repo/flathub.flatpakrepo"):
        self.__remote_name = remote_name

        self.__version = self.__get_flatpak__version()
        self.__add_remote(remote_name, remote_url)
        self.__installed_list = self.__generate_installed_list()
        self.__application_list = self.__generate_application_list(remote_name)
        self.__sort_application_list()

        print(self.__application_list)
        print(self.__installed_list)

    def __add_remote(self, remote_name, remote_url):
        return_value = subprocess.call(["flatpak", "remote-add", "--user", "--if-not-exists", remote_name, remote_url])
        if return_value != 0:
            raise Exception("Error: Failed to add remote {} with url {}".format(remote_name, remote_url))
        print("{} was successfully added".format(remote_name))

    def __generate_application_list(self, remote_name):
        command = ["flatpak", "remote-ls",remote_name,"--user", "--app"]
        application_list = []
        line_number = 1
        for line in subprocess.check_output(command).splitlines():
            if self.meets_version_requirement("1.1.0"):
                if line_number == 1:
                    line_number += 1
                    continue
                name_description, flatpak_id, version, branch = line.split("\t", 3)
                if "-" in name_description:
                    name, description = name_description.split("-", 1)
                else:
                    name = line.split(".")[-1]
                    description = ""

                installed = (flatpak_id in self.__installed_list)
                application = pyflatpak.application(flatpak_id, remote_name, name, installed, description, version=version)
            else:
                flatpak_id = line.strip()
                name = flatpak_id.split(".")[-1]
                installed = (flatpak_id in self.__installed_list)
                application = pyflatpak.application(flatpak_id, remote_name, name, installed)

            application_list.append(application)
            line_number += 1

        return application_list

    def __generate_installed_list(self):
        command = ["flatpak", "list","--user", "--app"]
        installed_list = []
        line_number = 1
        for line in subprocess.check_output(command).splitlines():
            if self.meets_version_requirement("1.1.0"):
                if line_number == 1:
                    line_number += 1
                    continue
                name_description, flatpak_id, version, branch, arch, origin = line.split("\t", 5)
                installed_list.append(flatpak_id)
            else:
                flatpak_id = line.strip()
                installed_list.append(flatpak_id)
            line_number += 1
        return installed_list

    def __get_flatpak__version(self):
        command = ["flatpak", "--version"]
        # First check if flatpak is installed
        return_value = subprocess.call(command)
        if return_value != 0:
            raise Exception("Error: Failed to run flatpak")
        output = subprocess.check_output(command).splitlines()
        version = output[0].split(" ")[1]
        print(version)
        return version

    def get_application_list(self):
        return self.__application_list

    def __sort_application_list(self):
        self.__application_list.sort()

    def meets_version_requirement(self, version):
        required = version.split(".")
        current = self.__version.split(".")

        meets_requirements = False
        if required[0] < current[0]:
            meets_requirements = True
        elif required[0] == current[0] and required[1] < current[1]:
            meets_requirements = True
        elif required[0] == current[0] and required[1] == current[1] and required[2] < current[2]:
            meets_requirements = True
        elif required[0] == current[0] and required[1] == current[1] and required[2] == current[2]:
            meets_requirements = True

        return meets_requirements

    def install(self, application):
        return_value = subprocess.call(["flatpak", "install", "--user", "-y", self.__remote_name, application.flatpak_id])
        if return_value != 0:
            raise Exception("Error: Failed to install application {}".format(application.flatpak_id))
        print("{} was successfully installed".format(application.flatpak_id))
        application.installed = True
        self.__sort_application_list()

    def uninstall(self, application):
        # 1.0.0 and newer requires the -y option
        if self.meets_version_requirement("1.0.0"):
            command = ["flatpak", "uninstall", "--user", "-y", application.flatpak_id]
        else:
            command = ["flatpak", "uninstall", "--user", application.flatpak_id]

        return_value = subprocess.call(command)
        if return_value != 0:
            raise Exception("Error: Failed to uninstall application {}".format(application.flatpak_id))
        print("{} was successfully uninstalled".format(application.flatpak_id))
        application.installed = False
        self.__sort_application_list()


    def __str__():
        return self.__remote_name
