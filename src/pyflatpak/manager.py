import subprocess
import pyflatpak

class manager():

    def __init__(self, remote_name="flathub", remote_url="https://dl.flathub.org/repo/flathub.flatpakrepo"):
        # Try to add the remote, just in case we don't have it yet
        self.__add_remote(remote_name, remote_url)

        self.__application_list = self.__generate_application_list(remote_name)

        self.__remote_name = remote_name

    def __add_remote(self, remote_name, remote_url):
        return_value = subprocess.call(["flatpak", "remote-add", "--user", "--if-not-exists", remote_name, remote_url])
        if return_value != 0:
            raise Exception("Error: Failed to add remote {} with url {}".format(remote_name, remote_url))
        print("{} was successfully added".format(remote_name))

    def __generate_application_list(self, remote_name):
        command = ["flatpak", "remote-ls",remote_name,"--user", "--app","--columns=application"]
        application_list = []
        for line in subprocess.check_output(command).splitlines():
            application_list.append(pyflatpak.application(line, remote_name))

        return application_list

    def get_application_list(self):
        return self.__application_list

    def __str__():
        return self.__remote_name
