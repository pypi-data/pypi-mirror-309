import hashlib
import json
import os
import getpass

from pykeepass import PyKeePass

from pathlib import Path
from typing import Optional


class MultipleConfJsonFilesError(Exception):
    """Exception raised when multiple 'conf.json' files are found."""

    pass


class ConnectionConf:
    def __init__(self, app, via_app) -> None:
        self.app = app
        self.conf = self._find_conf()
        self.via_app_server = via_app
        self.app_host = None
        self.db_host = None
        self.db_user = None
        self.database = None
        self.db_password = None
        self.tunnel_user = None
        self.db_port = None
        self.tunnel_port = None
        self._set_attributes()

    def _find_conf(self, base_path: Optional[Path] = None) -> Optional[Path]:
        if base_path is None:
            base_path = Path.cwd()

        if not base_path.is_dir():
            raise ValueError(f"Provided base path {base_path} is not a directory.")

        conf_files = list(base_path.rglob("conf.json"))

        if len(conf_files) > 1:
            raise MultipleConfJsonFilesError("Found more than one conf.json file")

        if len(conf_files) == 0:
            return None

        return conf_files[0]

    def _get_keepass_key(self):
        with open(
            os.path.expanduser("~/.ssh/id_rsa.pub"), "r", encoding="utf-8"
        ) as public_key_file:
            public_key = public_key_file.read()

        sha256_hash = hashlib.sha256()
        sha256_hash.update(public_key.encode("utf-8"))

        return sha256_hash.hexdigest()

    def _set_attributes(self):
        if self.conf:
            try:
                with self.conf.open("r") as conf:
                    servers = json.load(conf)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON from file {self.conf}: {e}")
            except IOError as e:
                raise ValueError(f"Error reading file {self.conf}: {e}")

            if servers:
                for server in servers:
                    if server.get("app_name") == self.app:
                        settings = server

                if settings.get("app_host"):
                    self.app_host = settings.get("app_host")

                if settings.get("db_host"):
                    self.db_host = settings.get("db_host")
                else:
                    # This might not be the case for SQLite
                    raise ValueError(
                        "db_host is a required variable if you are using a json file to build a connection"
                    )

                if settings.get("db_user"):
                    self.db_user = settings.get("db_user")

                if settings.get("database"):
                    self.database = settings.get("database")
                else:
                    # This might not be the case for SQLite
                    raise ValueError(
                        "database is a required variable if you are using a json file to build a connection"
                    )

                if settings.get("db_password"):
                    self.db_password = settings.get("db_password")

                if settings.get("tunnel_user"):
                    self.tunnel_user = settings.get("tunnel_user")

                if settings.get("db_port"):
                    self.db_port = settings.get("db_port")

                if settings.get("tunnel_port"):
                    self.tunnel_port = settings.get("tunnel_port")

        else:
            user = getpass.getuser().replace(".", "_")
            keepass_file_path = os.path.abspath(
                os.path.join("R:", "Connection Manager", user, f"{user}.kdbx ")
            )

            if not os.path.exists(keepass_file_path):
                raise FileExistsError(
                    "Can't find your keepass file. You might need to run rr-key-manager or connect to the vpn"
                )

            kp = PyKeePass(
                keepass_file_path,
                password=self._get_keepass_key(),
            )

            group = kp.find_groups(name=self.app, first=True)

            if not group:
                raise LookupError(
                    f"Could not find server {self.app} in keypass. Perhaps its the wrong name or needs to be added."
                )

            if any(e for e in group.entries if "db_server" in e.path):
                db_server = next((e for e in group.entries if "db_server" in e.path))
                self.db_host = db_server.url
                self.tunnel_user = db_server.username

                if db_server.notes and "PORTS" in db_server.notes:
                    self.db_port = json.loads(db_server.notes)["PORTS"]["DB_PORT"]
                    self.tunnel_port = json.loads(db_server.notes)["PORTS"]["SSH_PORT"]

            if any(e for e in group.entries if "db_user" in e.path):
                db_user = next((e for e in group.entries if "db_user" in e.path))
                self.db_user = db_user.username
                self.db_password = db_user.password

                if db_user.notes and "DATABASE" in db_user.notes:
                    self.database = json.loads(db_user.notes)["DATABASE"][0]

            if any(e for e in group.entries if "app_server" in e.path):
                app_server = next((e for e in group.entries if "app_server" in e.path))
                self.app_host = app_server.url

                if (
                    self.via_app_server == "true"
                    and app_server.notes
                    and "PORTS" in app_server.notes
                ):
                    self.tunnel_user = app_server.username
                    self.tunnel_port = json.loads(app_server.notes)["PORTS"]["SSH_PORT"]
