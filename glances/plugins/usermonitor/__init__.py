# 
#
# This is the new plugin created to implement feature request #1766.
#
# Active Users, User monitoring, and more
#
#

"""Active Users/User Monitoring Plugin."""

import psutil
from glances.plugins.plugin.model import GlancesPluginModel

class PluginModel(GlancesPluginModel):
    """
    PluginModel is a custom Glances plugin that retrieves and displays
    specific metrics.

    Inherits from GlancesPlugin and implements the required methods
    for updating and managing data.
    """
    def __init__(self, args=None, config=None):
        """
        Initialize the MyPlugin class with default values or configurations.
        """
        super().__init__(args=args)

    def update(self):
        """
        Update the plugin data by collecting metrics.

        This method should fetch new data and update the internal state
        of the plugin. Called periodically by Glances.
        """
