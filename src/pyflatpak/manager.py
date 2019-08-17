import subprocess
import pyflatpak

steamos_flatpak_version = "0.8.9"
#steamos_flatpak_version = "1.2.4" # actually Debian Buster's version

class manager():

    def __init__(self, remote_name="flathub", remote_url="https://dl.flathub.org/repo/flathub.flatpakrepo"):
        # Try to add the remote, just in case we don't have it yet
        self.__version = self.__get_flatpak__version()

        self.__add_remote(remote_name, remote_url)

        self.__application_list = self.__generate_application_list(remote_name)

        self.__remote_name = remote_name

    def __add_remote(self, remote_name, remote_url):
        return_value = subprocess.call(["flatpak", "remote-add", "--user", "--if-not-exists", remote_name, remote_url])
        if return_value != 0:
            raise Exception("Error: Failed to add remote {} with url {}".format(remote_name, remote_url))
        print("{} was successfully added".format(remote_name))

    def __generate_application_list(self, remote_name):
        if self.__version != steamos_flatpak_version:
            command = ["flatpak", "remote-ls",remote_name,"--user", "--app","--columns=application,description"]
        else:
            command = ["flatpak", "remote-ls",remote_name,"--user", "--app"]
        application_list = []
        line_number = 1
        for line in subprocess.check_output(command).splitlines():
            if line_number == 1:
                line_number += 1
                continue
            if self.__version != steamos_flatpak_version:
                id, description = line.split("\t")
                application_list.append(pyflatpak.application(id, remote_name, description))
            else:
                line_content = line.split(".")
                print(line_content)
                description = line_content[-1]
                application_list.append(pyflatpak.application(line, remote_name, description))
            line_number += 1

        return application_list

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

    def __str__():
        return self.__remote_name
