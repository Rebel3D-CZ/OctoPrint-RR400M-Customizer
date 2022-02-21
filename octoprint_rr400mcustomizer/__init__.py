# coding = utf-8

import octoprint.plugin
import sys
import logging
import flask
import netifaces as ni
import re
from octoprint.util import RepeatedTimer

__plugin_name__ = "RR400M Customizer"
__plugin_pythoncompat__ = ">=3.7,<4"

class RR400MCustomizerPlugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.AssetPlugin
):

    def get_settings_defaults(self):
        self._logger.info("%s: default called" % __plugin_name__)
        return dict(
            wifi=dict(
               ssid=self.wifi_ssid,
               psk=self.wifi_psk
            )
        )

    def on_settings_save(self, data):
        self._logger.info("%s: save called" % __plugin_name__)
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.wifi_ssid = self._settings.get(["wifi", "ssid"])
        self.wifi_psk = self._settings.get(["wifi", "psk"])
        with open('/opt/rebelove.org/var/updatewifi.lock', 'w') as f:
            f.write('ssid="%s"\n' % self.wifi_ssid)
            f.write('psk="%s"\n' % self.wifi_psk)


    def regex_kv_pairs(self, text, item_sep=r"\s", value_sep="="):
        """
        Parse key-value pairs from a shell-like text with regex.
        This approach is ~ 25 times faster than the shlex approach.
        Returns a dict with the keys and values from the text input
        """

        split_regex = r"""
            (?P<key>[\w\-]+)=       # Key consists of only alphanumerics and '-' character
            (?P<quote>["']?)        # Optional quote character.
            (?P<value>[\S\s]*?)     # Value is a non greedy match
            (?P=quote)              # Closing quote equals the first.
            ($|\s)                  # Entry ends with comma or end of string
        """.replace("=", value_sep).replace(r"|\s)", f"|{item_sep})")
        regex = re.compile(split_regex, re.VERBOSE)

        return {match.group("key"): match.group("value") for match in regex.finditer(text)}

    def __init__(self):
        self._updateTimer = None
        self.wifimode = None
        # Read WiFi config
        wificfg = '/etc/wpa_supplicant/wpa_supplicant-wlan0.conf'
        cfgfile = open(wificfg, 'r')
        Lines = cfgfile.readlines()
        cfgfile.close()

        # process lines
        self.wifi_ssid = ''
        self.wifi_psk = ''
        for line in Lines:
            m = self.regex_kv_pairs(line.strip())
            if 'ssid' in m:
                self.wifi_ssid = m['ssid']
            if 'psk' in m:
                self.wifi_psk = m['psk']
#        self._logger.info("RR400MCustomizer: WiFI %s/%s" % (wifi_ssid, wifi_pass))

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
                "custom_bindings": False,
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
            pass

        # detect wifi status
        try:
            self._logger.info("%s: WiFi in mode %s" % (__plugin_name__, self.wifimode))
            # test WLAN mode
            iface = ni.ifaddresses('wlan0')
            if ni.AF_INET in iface:
                sys_ip = iface[ni.AF_INET][0]['addr']
                # in AP mode
                if len(sys_ip) > 7 and self.wifimode != 'wlan':
                    self._logger.debug("RR400mMCstomizer: WiFi switched to WLAN mode")
                    self.wifimode = 'wlan'
                    octoprint.printer.commands("M118 A1 P0 action.notification SSID %s IP %s" % ("?ssid?", sys_ip))
#                    self._logger.info("%s: GCODE WLAN ip=%s" % (__plugin_name__, sys_ip))
                return

            # test AP mode
            sys_ip = ni.ifaddresses('ap0')[ni.AF_INET][0]['addr']
            if len(sys_ip) > 7:
                # in AP mode
                if self.wifimode != 'ap':
                    self._logger.debug("RR400mMCstomizer: WiFi switched to AP mode")
                    self.wifimode = 'ap'
                    octoprint.printer.commands("M118 A1 P0 action.notification IP %s" % (sys_ip))
#                    self._logger.info("%s: GCODE AP ip=%s" % (__plugin_name__, sys_ip))
                return
        except Exception as exc:
#            self._logger.info(f"RR400MCustomizer: timer exception: %s" % str(exc))
            self._logger.info(f"RR400MCustomizer: timer exception: {exc.args}")
            pass

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
