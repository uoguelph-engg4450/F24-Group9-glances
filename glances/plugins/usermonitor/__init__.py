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

# Global variable definition for Field Description
fields_description = {
    'name': {
        'description': 'User Name',  # Human-readable name for the field
        'align': 'left',            # Text alignment in the curses UI 
        'color': 'WHITE',           # Color for the field text
        'type': 'str',              # Type of data 
    },
    'started': {
        'description': 'Started At',
        'align': 'right',
        'color': 'GREEN',
        'type': 'str',
    },
    'cpu': {
        'description': 'CPU %',
        'align': 'right',
        'color': 'YELLOW',
        'type': 'float',
    },
    'memory': {
        'description': 'Memory %',
        'align': 'right',
        'color': 'MAGENTA',
        'type': 'float',
    },
}


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
        super().__init__(args=args, config=config, fields_description=fields_description)
        self.active_users = []
        self.logger = getattr(self, 'logger', logging.getLogger(__name__))
        self.data = []

        #We want to display the stat in the curse interface
        self.display_curse = True


    @GlancesPluginModel._check_decorator
    @GlancesPluginModel._log_result_decorator
    def update(self):
        """
        Update the plugin data by collecting metrics.

        This method should fetch new data and update the internal state
        of the plugin. Called periodically by Glances.
        """
        try:
            self.active_users = psutil.users()
            user_stats = {}

            for user in self.active_users:
                if user.name not in user_stats:
                    user_stats[user.name] = {'cpu': 0.0, 'memory': 0.0}

            # Collect CPU and memory usage by user
            for proc in psutil.process_iter(['username', 'cpu_percent', 'memory_percent']):
                username = proc.info['username']
                if username in user_stats:
                    user_stats[username]['cpu'] += proc.info['cpu_percent']
                    user_stats[username]['memory'] += proc.info['memory_percent']

            self.data = [
                {
                    'name': user.name,
                    'started': datetime.datetime.fromtimestamp(user.started).strftime('%Y-%m-%d %H:%M:%S'),
                    'cpu': user_stats[user.name]['cpu'],
                    'memory': user_stats[user.name]['memory'],
                }
                for user in self.active_users
            ]
            self.logger.debug(f"Collected active users: {self.data}")
            return self.data
        except Exception as e:
            self.logger.debug(f"Failed to update usermonitor Plugin: {e}")
            return None

    def update_views(self):
        """Update stats views."""

        super().update_views()

        for user in self.data:
            user_key = user['name']
            self.views[user_key] = {
                'cpu': {'decoration': self.get_alert(user['cpu'], header='cpu')},
                'memory': {'decoration': self.get_alert(user['memory'], header='memory')},
            }
    def msg_curse(self, args=None, max_width=None):
        """Return the string to display in the curse interface."""
        ret = []  # Initializing

        # if no data or plugin disabled, return the empty list
        if not self.data or self.is_disabled():
            return ret

        # title line
        ret.append(self.curse_add_line("Active Users", "TITLE"))

        # loop through collected user data and format user details
        for user in self.data:
            user_info = (
                f"{user['name']:10}{user['started']:20}"
                f"CPU: {user['cpu']:6.2f}% Mem: {user['memory']:6.2f}%"
            )
            # if max_width provided, truncate line to fit screen width
            if max_width and len(user_info) > max_width:
                user_info = user_info[:max_width - 3] + "..."
            ret.append(self.curse_add_line(user_info))

        return ret
    
