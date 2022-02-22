# coding utf-8

###############################################################################

plugin_identifier = "rr400mcustomizer"
plugin_package = "octoprint_{}".format(plugin_identifier)
plugin_name = "RR400M Customizer"
plugin_version = "0.2.2"
plugin_description = "Adjustments of OctoPrint for 3D printer RR400M with BTT TFT50 LCD"
plugin_author = "Camel1cz"
plugin_author_email = "camel@camel.cz"
plugin_url = "https://github.com/Rebel3D-CZ/OctoPrint-RR400M-Customizer"
plugin_license = "AGPLv3"
plugin_copyright = (
    "Copyright (C) Rebel3D - Released under terms of the AGPLv3 License"
)
plugin_requires = ["netifaces>=0.10.9,<1"]
plugin_additional_data = []
plugin_additional_packages = []
plugin_ignored_packages = []
additional_setup_parameters = {"python_requires": ">3.7,<4"}

###############################################################################

from setuptools import setup

try:
    import octoprint_setuptools
except:
    print(
        "Could not import OctoPrint's setuptools, are you sure you are running that under "
        "the same python installation that OctoPrint is installed under?"
    )
    import sys

    sys.exit(-1)

setup_parameters = octoprint_setuptools.create_plugin_setup_parameters(
    identifier=plugin_identifier,
    package=plugin_package,
    name=plugin_name,
    version=plugin_version,
    description=plugin_description,
    author=plugin_author,
    mail=plugin_author_email,
    url=plugin_url,
    license=plugin_license,
    requires=plugin_requires,
    additional_packages=plugin_additional_packages,
    ignored_packages=plugin_ignored_packages,
    additional_data=plugin_additional_data,
)

if len(additional_setup_parameters):
    from octoprint.util import dict_merge

    setup_parameters = dict_merge(setup_parameters, additional_setup_parameters)

setup(**setup_parameters)
