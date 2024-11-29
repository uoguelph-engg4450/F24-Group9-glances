#
#
# This is the new plugin created to implement feature request #1766.
#
# Active Users, User monitoring, and more
#
#

"""Active Users/User Monitoring Plugin."""

import datetime
import logging

import psutil

from glances.plugins.plugin.model import GlancesPluginModel

# Global variable definition for Field Description
fields_description = {
    'name': {
        'description': 'User Name',  # Human-readable name for the field
        'align': 'left',  # Text alignment in the curses UI
        'color': 'WHITE',  # Color for the field text
        'type': 'str',  # Type of data
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

        # We want to display the stat in the curse interface
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
                    'started': datetime.datetime.fromtimestamp(user.started).strftime('%Y-%m-%d'),
                    'cpu': user_stats[user.name]['cpu'],
                    'memory': user_stats[user.name]['memory'],
                }
                for user in self.active_users
            ]

            self.stats = self.data
            self.logger.debug(f"Collected active users: {self.data}")
            # return self.data
            return self.stats

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
        """Return the dict to display in the curse interface."""
        # Initialize the return list
        ret = []

        # Only process if data exists and the plugin is enabled
        if not self.data or self.is_disabled():
            return ret

        # Define consistent column widths
        name_max_width = 10
        started_width = 10  # Width for the 'Started' column
        cpu_width = 7       # Width for the 'CPU %' column
        mem_width = 6       # Width for the 'Mem %' column

        # Header
        header = (
            f"{'ACTIVE':<{name_max_width}} "
            f"{'STARTED':<{started_width}} "
            f"{'CPU %':>{cpu_width}} "
            f"{'MEM %':>{mem_width}}"
        )
        ret.append(self.curse_add_line(header, "TITLE"))

        # Stats
        for user in self.data:
            ret.append(self.curse_new_line())
            try:
                # Format each row
                user_row = (
                    f"{user['name'][:name_max_width]:<{name_max_width}} "  # Username
                    f"{user['started']:<{started_width}} "               # Start time
                    f"{user['cpu']:>{cpu_width}.2f} "                    # CPU %
                    f"{user['memory']:>{mem_width}.2f}"                  # Mem %
                )
                # Append the formatted row to the result
                ret.append(self.curse_add_line(user_row))
            except KeyError as e:
                self.logger.error(f"Missing key in user data: {e}")
                continue
            except (TypeError, ValueError) as e:
                self.logger.error(f"Error formatting user data: {e}")
                continue

        # Add a blank line at the end for better formatting
        ret.append(self.curse_new_line())

        return ret






