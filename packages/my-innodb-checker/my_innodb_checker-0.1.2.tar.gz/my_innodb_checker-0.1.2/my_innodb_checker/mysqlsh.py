"""
module to wrap mysqlsh
"""

import json
import os
import subprocess
import sys
from logging import getLogger
from typing import Optional, Union

from tabulate import tabulate

from .constants import (
    CheckStatus,
    ClusterDict,
    MemberRole,
    MemberStatus,
    MyLogin,
    NodeDict,
)

_logger = getLogger(__name__)

MYSQLSH_PATH = "/usr/bin/mysqlsh"


class MysqlSh:

    def __init__(self, logins: Optional[Union[MyLogin, str]] = None):
        self._path = MYSQLSH_PATH
        if not os.path.isfile(self._path):
            _logger.error("mysqlsh at %s doesn't exist or it's not a file", self._path)
            sys.exit(CheckStatus.UNKNOW.value)
        self._logins = logins
        self._node_results: list = []
        self._cluster_results: ClusterDict = {}

    def _execute_cli(self, cli: list) -> dict:
        """
        Method to execute shell command
        """
        _logger.debug("executing: %s", " ".join(cli))
        with subprocess.Popen(cli, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as c:
            output, error = c.communicate()
        if error:
            _logger.error(error.decode())
            sys.exit(CheckStatus.UNKNOW.value)
        return json.loads(output.decode())

    def __cluster_status_cli(self) -> list:
        """
        Method to format cluster check cli command
        """
        cli = [self._path]
        if isinstance(self._logins, str):
            cli.append(f"--defaults-file={self._logins}")
        else:
            assert isinstance(self._logins, dict)
            cli.append("--host")
            cli.append(self._logins["host"])
            cli.append("--port")
            cli.append(str(self._logins["port"]))
            cli.append("--user")
            cli.append(self._logins["user"])
            password = self._logins["password"]
            cli.append(f"--password={password}")
        cli.append("--")
        cli.append("cluster")
        cli.append("status")
        return cli

    def cluster_status(self):
        """
        CLuster check method
        """
        cli = self.__cluster_status_cli()
        output = self._execute_cli(cli)
        self._cluster_results["name"] = output.get("clusterName")
        self._cluster_results["role"] = output.get("clusterRole")
        replica = output.get("defaultReplicaSet")
        self._cluster_results["status"] = replica.get("status")
        self._cluster_results["topology"] = replica.get("topologyMode")
        self._cluster_results["message"] = replica.get("statusText")
        topology = replica.get("topology")
        for k, v in topology.items():
            lag = v.get("replicationLagFromImmediateSource")
            primary = MemberRole[v.get("memberRole")].value
            r: NodeDict = {
                "node": k.split(":")[0],
                "primary": primary,
                "mode": v.get("mode"),
                "status": v.get("status"),
                "version": v.get("version"),
                "lag": lag if lag or primary else "00:00:00.000000",
            }
            self._node_results.append(r)

        print(tabulate([self._cluster_results], headers="keys"), end="\n\n")
        print(tabulate(self._node_results, headers="keys"))
        self._exit_status()

    def _exit_status(self) -> None:
        """
        method to parse exit status from results
        """
        exit_status = CheckStatus[self._cluster_results.get("status")].value  # type: ignore
        for s in self._node_results:
            node_status = MemberStatus[s.get("status")].value
            exit_status = max(exit_status, CheckStatus[node_status].value)
        sys.exit(exit_status)
