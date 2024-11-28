import logging
from glances.plugins.usermonitor import PluginModel  

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def test_plugin():
    """
    Test the PluginModel class by instantiating it and calling update().
    """
    print("Testing Active Users Plugin...")

    # Create an instance of the plugin
    plugin = PluginModel()

    # Call the update method
    data = plugin.update()

    # Display the collected data
    if data:
        print("Active Users:")
        for user in data:
            print(
                f"Name: {user['name']}, "
                f"Started: {user['started']}, "
                f"CPU: {user['cpu']:.2f}%, "
                f"Memory: {user['memory']:.2f}%"
            )
    else:
        print("No active users or an error occurred.")

if __name__ == "__main__":
    test_plugin()
