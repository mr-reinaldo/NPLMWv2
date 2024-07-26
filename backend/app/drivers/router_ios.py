from app.drivers.base_netmiko import NetmikoDriver
from app.schemas.netmiko_schemas import NetmikoConn

# ntc-templates: https://github.com/networktocode/ntc-templates/tree/master/ntc_templates/templates


class RouterIOS(NetmikoDriver):

    def __init__(self, device: NetmikoConn):
        super().__init__(device)

    def connect(self):
        super().connect()

    def disconnect(self):
        super().disconnect()

    def get_interfaces(self):
        output = self._net_connect.send_command("show ip int brief", use_textfsm=True)
        return output

    def get_version(self):
        output = self._net_connect.send_command("show version", use_textfsm=True)
        return output

    def get_running_config(self):
        output = self._net_connect.send_command("show running-config")
        return output

    def get_arp_table(self):
        output = self._net_connect.send_command("show ip arp", use_textfsm=True)
        return output

    def get_ip_routers(self):
        output = self._net_connect.send_command("show ip route", use_textfsm=True)
        return output
