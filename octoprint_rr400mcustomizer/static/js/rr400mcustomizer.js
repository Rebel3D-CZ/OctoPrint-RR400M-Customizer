$(function () {
  function RR400MCustomizerViewModel(parameters) {
    var self = this;

    self.settingsViewModel = parameters[0];

    self._svgPrefix = '<path d="M0 0h24v24H0z" fill="none"/>';
    self._iconSVGs = [
      '<text xml:space="preserve" text-anchor="start" font-family="\'Antonio\'" font-size="24" id="svg_5" y="21" x="5.00002" stroke="#0660e6" fill="#0660e6">R</text>',
    ];

    self.IconSVG = ko.observable(self._svgPrefix + self._iconSVGs[0]);
    self.interfaces = ko.observableArray([]);
    self.popoverContent = ko.observable(
      '<table style="width: 100%"><thead></thead><tbody><tr><td>&copy; 2022 Rebel3D</td></tr></tbody></table>'
    );

    self.settings = undefined;

    self.onAfterBinding = function () {};
    self.onBeforeBinding = function () {
        self.settings = self.settingsViewModel.settings.plugins.rr400mcustomizer;
    };

    self.refreshWiFi = function (plugin, data) {
      console.log("refresh called")
    }

    self.onDataUpdaterPluginMessage = function (plugin, data) {
      if (plugin != "rr400mcustomizer") {
        return;
      }
      svg = self._svgPrefix;

      var pluginData = '<table style="width: 100%"><thead></thead><tbody>';
      if (data.clientid) {
        svg += self._iconSVGs[0];
        pluginData += "<tr><td>Client ID</td><td>" + data.clientid + "</td></tr>";
      }
      if (data.ssids) window.ssids = data.ssids
      pluginData += "<tr><td>&copy; 2022 Rebel3D</td></tr>";
      pluginData += "</tbody></table>";
      self.IconSVG(svg);
      self.popoverContent(pluginData);
    };

    $('#rr400m_refreshWiFi').click(function () {
      console.dir("button presed");
      $('#settings_plugin_rr400mcustomizer #available-ssids').html(window.ssids.join('<br>'))
      return false;
    });
  }

  OCTOPRINT_VIEWMODELS.push({
    construct: RR400MCustomizerViewModel,
    dependencies: ["settingsViewModel"],
    elements: ["#navbar_plugin_rr400mcustomizer"],
  });
});
