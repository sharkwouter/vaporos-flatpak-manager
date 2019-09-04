import requests
import vfmflathub


def get_applications():
    url = "https://flathub.org/api/v1/apps"
    params = {}
    response = requests.get(url, params=params)

    applications = []
    installed_applications = vfmflathub.get_installed_applications()
    print(installed_applications)

    # Create application objects based on the data received from the API
    for entry in response.json():
        app_id = entry['flatpakAppId']
        name = entry['name'].encode('utf-8')
        description = entry['summary'].encode('utf-8')
        version = entry['currentReleaseVersion']
        image_url = entry['iconDesktopUrl']

        # Check if application is installed
        if app_id in installed_applications:
            installed = True
        else:
            installed = False

        application = vfmflathub.Application(app_id, name, description, version, image_url, installed)
        applications.append(application)

    return applications


