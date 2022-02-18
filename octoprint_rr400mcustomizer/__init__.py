# coding = utf-8

import octoprint.plugin
import sys
import logging
import flask
import netifaces as ni
from octoprint.util import RepeatedTimer

__plugin_name__ = "RR400M Customizer"
__plugin_pythoncompat__ = ">=3.7,<4"

class RR400MCustomizerPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.SettingsPlugin,
#    octoprint.plugin.SimpleApiPlugin,
):

    def __init__(self):
        self._updateTimer = None

    def on_after_startup(self):
        self._logger.info("%s v%s started!" % (__plugin_name__, self._plugin_version))
        self.start_update_timer(10.0)

    def get_assets(self):
        return {
            "js": ["js/rr400mcustomizer.js"],
            "css": ["css/rr400mcustomizer.css"],
        }

    def get_template_configs(self):
        return [
            {
                "type": "navbar",
                "custom_bindings": True,
                "classes": [
                    "dropdown",
                ],
            },
            {
                "type": "settings",
                "custom_bindings": True,
            },
        ]

    def update_rr400mcustomizer_status(self):
        self._logger.debug("RR400mMCstomizer: update fired!")
        try:
            plugin_data = {}

            plugin_data["clientid"] = ni.ifaddresses('tun0')[ni.AF_INET][0]['addr'].split(".")[3]

            self._logger.debug(plugin_data)

            self._plugin_manager.send_plugin_message(self._identifier, plugin_data)
        except Exception as exc:
            self._logger.debug(f"RR400MCustomizer: timer exception: {exc.args}")

    def start_update_timer(self, interval):
        self._updateTimer = RepeatedTimer(
            interval, self.update_rr400mcustomizer_status, run_first=True
        )
        self._updateTimer.start()
        self._logger.debug("RR400MCustomizer: started timer!")

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

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = RR400MCustomizerPlugin()

    # ~~ Softwareupdate hook

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
