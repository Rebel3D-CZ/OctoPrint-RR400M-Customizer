# coding = utf-8

import octoprint.plugin
import sys
import logging
import flask
import netifaces as ni
from octoprint.util import RepeatedTimer


class RR400MCustomizerPlugin(
#    octoprint.plugin.StartupPlugin,
#    octoprint.plugin.TemplatePlugin,
#    octoprint.plugin.AssetPlugin,
#    octoprint.plugin.SettingsPlugin,
#    octoprint.plugin.SimpleApiPlugin,
):


    def get_update_information(self):
        return {
            "rr400mcustomizer": {
                "displayName": "RR400M Customizer",
                "displayVersion": self._plugin_version,
                # version check: github repository
                "type": "github_release",
                "user": "Rebel3D-CZ",
                "repo": "OctoPrint-RR400M-Customizer",
                "current": self._plugin_version,
                # update method: pip w/ dependency links
                "pip": "https://github.com/Rebel3D-CZ/OctoPrint-RR400M-Customizer/archive/{target_version}.zip",
            }
        }

__plugin_name__ = "RR400M Customizer"
__plugin_pythoncompat__ = ">=3.7,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = RR400MCustomizerPlugin()

    # ~~ Softwareupdate hook

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
