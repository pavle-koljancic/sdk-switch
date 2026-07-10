import logging
import time
from logging import Logger

import paramiko
from paramiko import Channel
from paramiko import SSHClient

BUFFER_SIZE = 1024


class ActiveShhClient(SSHClient):
    def __init__(self, logger: Logger | None = None):
        super().__init__()
        self.load_system_host_keys()  # uses ~/.ssh/known_hosts
        self.set_missing_host_key_policy(paramiko.WarningPolicy)
        self.history: list[tuple[str, list[str]]] = []
        self.__of_shell: Channel
        self.device_prompt: str = ""
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__ + ".null")
            self.logger.addHandler(logging.NullHandler())
        self.tunnel: Channel | None = None
        self.jump_client: SSHClient | None = None

    def history_append(self, command: str, output: list[str]) -> None:
        if (not command) and (not output):
            return

        if command:
            self.logger.info(f"Executing:{command}")
        output_log = "\n".join(output)
        self.logger.info(f"Output:\n{output_log}")
        self.history.append((command, output))

    def wait_receive(self, timeout: float = 1) -> list[str]:
        """
        Read from Paramiko shell until no new data arrives for `timeout` seconds.
        """

        end_time = time.time() + timeout
        output = ""
        while True:
            if self.__of_shell.recv_ready():
                chunk = self.__of_shell.recv(BUFFER_SIZE).decode()
                output += chunk
                end_time = time.time() + timeout  # reset timer when data is coming
            else:
                if time.time() > end_time:
                    break
                time.sleep(0.05)
        return output.splitlines()

    def establish_connection(self, hostname: str, port: int, username: str, password: str, timeout: float = 60) -> None:
        self.logger.info(f"Connecting to {username}@{hostname}...")

        if self.tunnel is not None:
            self.connect(hostname, port=port, username=username, password=password, sock=self.tunnel, timeout=timeout)
        else:
            self.connect(hostname, port=port, username=username, password=password, timeout=timeout)

        self.logger.info("Connection established successfully.")
        self.__of_shell = self.invoke_shell()
        output = self.wait_receive(2)
        self.device_prompt = output.pop()
        self.history_append("", output)

    def filter_output(self, command: str, unfiltered_output: list[str]) -> list[str]:
        if len(unfiltered_output) == 0:
            return unfiltered_output  # No output
        if unfiltered_output[0] == command:
            unfiltered_output.remove(command)
            if len(unfiltered_output) == 0:
                return unfiltered_output  # Only the command was echoed back at us.
        if unfiltered_output[-1] == self.device_prompt:
            unfiltered_output.pop()
        cleaned_list = [s for s in unfiltered_output if s.strip() != ""]
        return cleaned_list

    def run(self, command: str) -> list[str]:
        # self.__of_shell.send("screen-length 0 temporary\n")
        self.__of_shell.send((command + "\n").encode())
        unfiltered_output = self.wait_receive()
        output = self.filter_output(command, unfiltered_output)
        self.history_append(command, output)
        return output

    def add_tunnel(
        self, jump_host: str, jump_username: str, jump_password: str, dest_host: str, dest_port: int = 22
    ) -> None:
        self.jump_client = SSHClient()
        self.jump_client.load_system_host_keys()  # uses ~/.ssh/known_hosts
        self.jump_client.set_missing_host_key_policy(paramiko.WarningPolicy)
        self.jump_client.connect(hostname=jump_host, username=jump_username, password=jump_password)
        transport = self.jump_client.get_transport()
        if not transport:
            raise ConnectionError("Could not get tunnel transport!")
        self.tunnel = transport.open_channel(
            "direct-tcpip",
            dest_addr=(dest_host, dest_port),
            src_addr=("localhost", 0),  # To make so that the Router sees the connection as coming from the VM
        )
        self.logger.info(f"Opened tunnel from {jump_username}@{jump_host} to {dest_host}:{dest_port} ")

    def close(self) -> None:
        super().close()
        if self.jump_client:
            if self.tunnel is not None:
                self.tunnel.close()
            self.jump_client.close()
