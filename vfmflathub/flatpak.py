import subprocess


def add_flathub():
    name = "flathub"
    url = "https://dl.flathub.org/repo/flathub.flatpakrepo"
    return_value = subprocess.call(["flatpak", "remote-add", "--user", "--if-not-exists", name, url])
    if return_value != 0:
        raise Exception("Error: Failed to add remote {} with url {}".format(name, url))
    print("{} was successfully added".format(name))


def get_installed_applications():
    command = ["flatpak", "list","--user", "--app"]
    installed_list = []
    for line in subprocess.check_output(command).splitlines():
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        if meets_version_requirement("1.1.0"):
            name_description, flatpak_id, version, branch, arch, origin = line.split("\t", 5)
            installed_list.append(flatpak_id)
        else:
            flatpak_id = line.strip()
            installed_list.append(flatpak_id)
    return installed_list


def get_flatpak_version():
    command = ["flatpak", "--version"]
    # First check if flatpak is installed
    return_value = subprocess.call(command)
    if return_value != 0:
        raise Exception("Error: Failed to run flatpak")
    output = subprocess.check_output(command).splitlines()
    version_string = output[0].decode("utf-8")
    version = version_string.split(" ")[1]
    return version


def meets_version_requirement(version):
    current = get_flatpak_version().split(".")
    required = version.split(".")

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


def install(application):
    return subprocess.Popen(["flatpak", "install", "--user", "-y", "flathub", application.flatpak_id], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def uninstall(application):
    # 1.0.0 and newer requires the -y option
    if meets_version_requirement("1.0.0"):
        command = ["flatpak", "uninstall", "--user", "-y", application.flatpak_id]
    else:
        command = ["flatpak", "uninstall", "--user", application.flatpak_id]
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
