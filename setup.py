from setuptools import setup, find_packages
setup(
    name="VaporOS-flatpak-manager",
    version="1.0",
    packages=find_packages(),
    scripts=["vaporos-flatpak-manager"],

    data_files = [
        ('', ['LICENSE']),
        ('share/applications', ['data/vaporos-flatpak-manager.desktop']),
        ('share/pixmaps', ['data/vaporos-flatpak-manager.png']),
    ],

    #metadata
    author="Wouter wijsman",
    author_email="wwijsman@live.nl",
    description="A flatpak frontend for SteamOS",
    keywords="flatpak steamos vaporos installer",
    url="http://vaporos.net/",
    license='MIT',
    project_urls={
        "Bug Tracker": "https://github.com/sharkwouter/vaporos-flatpak-manager/issues",
        "Documentation": "https://github.com/sharkwouter/vaporos-flatpak-manager/blob/master/README.md",
        "Source Code": "https://github.com/sharkwouter/vaporos-flatpak-manager",
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ]
)
