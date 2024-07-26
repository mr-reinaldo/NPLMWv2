from abc import ABC, abstractmethod
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko.exceptions import NetmikoTimeoutException
from netmiko.exceptions import SSHException
from app.schemas.netmiko_schemas import NetmikoConn

# Netmiko creator site: https://pynet.twb-tech.com/network-automation-articles.html


class NetmikoDriver(ABC):

    def __init__(self, device: NetmikoConn):
        self._device = device
        self._net_connect = None

    @abstractmethod
    def connect(self):
        try:
            self._net_connect = ConnectHandler(**self._device)

        except NetmikoAuthenticationException as err:
            print(err)

        except NetmikoTimeoutException as err:
            print(err)

        except SSHException as err:
            print(err)
        except ValueError as err:
            print(err)
        except Exception as err:
            print(f"Erro desconhecido: {err}")

    @abstractmethod
    def disconnect(self):
        self._net_connect.disconnect()
