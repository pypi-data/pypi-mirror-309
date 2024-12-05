# -*- coding: utf-8 -*-

from typing import Dict, Iterator, Tuple, List

from paramiko import Transport, RSAKey
from paramiko.sftp_attr import SFTPAttributes
from paramiko.sftp_client import SFTPClient
from paramiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import BadHostKeyException
from paramiko.ssh_exception import NoValidConnectionsError
from paramiko.ssh_exception import SSHException


class SftpClient:
    """
    SFTP Client.

    Example # 1 -> How to use it...
    *************************************************************************

    client = SFTPClient("test.rebex.net", "demo", "password")
    client.connect()

    for x in client.list_files("/"):
        print(x)

    client.close()

    Example # 2 -> How to use it...
    *************************************************************************

    with SFTPClient("test.rebex.net", "demo", "password") as _client:
        _client.download_file("readme.txt", "/tmp/readme.txt")

    Example # 3 -> Locally...
    *************************************************************************
    docker run -v /home/alejandro/Documents:/home/foo/upload \
               -p 22:22 \
               -d atmoz/sftp foo:pass:::upload

    ---> Using ssh key:
    docker run -v <host-dir>ssh/keys/id_rsa.pub:/home/foo/.ssh/keys/id_rsa.pub:ro \
               -v /home/alejandro/Documents:/home/foo/upload \
               -p 22:22 \
               -d atmoz/sftp foo::1001

    client = SftpClient("localhost", 22,"foo", "pass")
    client.connect()

    client.client.chdir("/upload")
    print(client.client.getcwd())

    for x in client.list_files("/upload/"):
        print(x)

    client.close()
    """

    def __init__(
            self, host: str, port: int = 22, user: str = None, password: str = None,
            private_key_path: str = None, transport_kwargs: Dict = None,
            connection_kwargs: Dict = None, disabled_algorithms: bool = False,
            algorithms_to_disable: List[str] = None):

        """
        :param host: Host or IP of the remote machine.
        :param user: Username at the remote machine.
        :param password: Password at the remote machine.
        :param private_key_path: Path to private key file.
        :param transport_kwargs: Named arguments for transport.
        :param connection_kwargs: Named arguments for connection.

        :param disabled_algorithms: If true, a list of algorithms will be disabled.
        :param algorithms_to_disable: Algorithms to disable.
        """

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.private_key_path = private_key_path

        self.connection_kwargs = connection_kwargs or {}
        self.transport_kwargs = transport_kwargs or {}
        self._sftp_client = None

        # It's a bug in Paramiko. It does not handle correctly absence
        # of server-sig-algs extension on the server side...
        # https://stackoverflow.com/questions/70565357/paramiko-authentication-fails-with-agreed-upon-rsa-sha2-512-pubkey-algorithm
        if disabled_algorithms:
            self.transport_kwargs["disabled_algorithms"] = {
                "pubkeys": algorithms_to_disable or ["rsa-sha2-512", "rsa-sha2-256"]
            }

    @property
    def client(self):
        """
        It provides access to the underline client to call methods that
        are not exposed via the wrapper...
        """

        return self._sftp_client

    def __enter__(self):
        self.connect()
        return self

    def connect(self):
        data = {
            "username": self.user,
            "password": self.password
        }

        try:
            if self.private_key_path:
                data["pkey"] = RSAKey.from_private_key_file(self.private_key_path)

            transport = Transport(
                (self.host, self.port),  # type: ignore
                **self.transport_kwargs)

            transport.connect(**data, **self.connection_kwargs)
            self._sftp_client = SFTPClient.from_transport(transport)
            return self

        except AuthenticationException as error:
            raise SftpClientError(f"Authentication error: {error}.")

        except BadHostKeyException as error:
            raise SftpClientError(f"HostKeys error: {error}.")

        except SSHException as error:
            raise SftpClientError(f"SSH error: {error}.")

        except NoValidConnectionsError as error:
            raise SftpClientError(f"Connection error: {error}")

        except Exception as error:
            raise SftpClientError(f"Error: {error}.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def list_files(self, remote_path) -> Iterator[Tuple[str, SFTPAttributes]]:
        """
        Read files under a remote directory...

        :param remote_path: Remote directory path.
        :return: Iterator of tuples in the form ("file_name", SFTPAttributes)
        """

        try:
            self._sftp_client.chdir(remote_path)
            for attr in self._sftp_client.listdir_attr():
                yield attr.filename, attr

        except IOError as error:
            raise SftpClientError(f"Error accessing directory: {error}")

    def download_file(self, remote_file_path, local_file_path):
        try:
            self._sftp_client.get(remote_file_path, local_file_path)
            return local_file_path

        except IOError as error:
            raise SftpClientError(f"Error downloading file: {error}")

    def close(self):
        if self._sftp_client:
            self._sftp_client.close()


class SftpClientError(Exception):
    """ Custom exception for SFTP Connection """
