from app.drivers.base_netmiko import NetmikoDriver


class Switch(NetmikoDriver):

    def __init__(self, device):
        super().__init__(device)

    def configure_vlan(self, vlan_id, vlan_name):

        cfg_commands = [f"vlan {vlan_id}", f"name {vlan_name}"]

        self.connection.send_config_set(cfg_commands)
        self.connection.save_config()
        self.connection.disconnect()
