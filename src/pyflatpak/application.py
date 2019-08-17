import subprocess


class application():

    def __init__(self, id, remote, description=""):
        self.__remote = remote
        self.__id = id
        self.__description = description

    def __get_description(self, remote, id):
        if self.__description:
            return self.__description

        command = ["flatpak", "remote-info", "--user", remote, id]
        for line in subprocess.check_output(command).splitlines():
            if " - " in line:
                self.__description = line
                break
        if not self.__description:
            self.__description = id
        return self.__description

    def install(self):
        return_value = subprocess.call(["flatpak", "install", "--user", "-y", self.__remote, self.__id])
        if return_value != 0:
            raise Exception("Error: Failed to install application {}".format(self.__id))
        print("{} was successfully installed".format(self.__id))

    def uninstall(self):
        return_value = subprocess.call(["flatpak", "uninstall", "--user", "-y", self.__id])
        if return_value != 0:
            raise Exception("Error: Failed to uninstall application {}".format(self.__id))
        print("{} was successfully uninstalled".format(self.__id))

    def __str__(self):
        return self.__get_description(self.__remote, self.__id)
