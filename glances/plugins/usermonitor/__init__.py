# 
#
# This is the new plugin created to implement feature request #1766.
#
# Active Users, User monitoring, and more
#
#

"""Active Users/User Monitoring Plugin."""
import logging
import datetime
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
        self.active_users = []
        self.logger = getattr(self, 'logger', logging.getLogger(__name__))
        self.data = []

    def update(self):
        """
        Update the plugin data by collecting metrics.

        This method should fetch new data and update the internal state
        of the plugin. Called periodically by Glances.
        """
        try:
            #Collect active users using psutil
            self.active_users = psutil.users()
            self.data = [
                {
                    'name': user.name, 
                    'terminal': user.terminal, 
                    'started': datetime.datetime.fromtimestamp(user.started).strftime('%Y-%m-%d %H:%M:%S')
                } 
                for user in self.active_users
            ]
            self.logger.debug(f"Collected active users: {self.data}")
            return self.data
        except Exception as e:
            self.logger.debug(f"Failed to update usermonitor Plugin: {e}")
            return None
        
