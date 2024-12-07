"""
module to wrap mysqlsh
"""

import json
import os
import subprocess
import sys
from logging import getLogger
from typing import Optional, Union

from tabulate import tabulate  # type: ignore

from .constants import (
    CheckStatus,
    ClusterDict,
    ClusterReplicaStatus,
    ClustersetBaseStatus,
    ClustersetDict,
    ClustersetGlobalStatus,
    ClustersetStatus,
    MemberRole,
    MemberStatus,
    MyLogin,
    NodeDict,
)

_logger = getLogger(__name__)

MYSQLSH_PATH = "/usr/bin/mysqlsh"


class MysqlSh:
    """
    class to wrap mysqlsh status output
    """

    def __init__(self, logins: Optional[Union[MyLogin, str]] = None):
        if not os.path.isfile(MYSQLSH_PATH):
            _logger.error(
                "mysqlsh at %s doesn't exist or it's not a file", MYSQLSH_PATH
            )
            sys.exit(CheckStatus.UNKNOW.value)
        self._logins = logins
        self._node_results: list = []
        self._cluster_results: ClusterDict = {}
        self._clusterset_members: list = []
        self._cli = [MYSQLSH_PATH]
        if isinstance(self._logins, str):
            self._cli.append(f"--defaults-file={self._logins}")
        else:
            assert isinstance(self._logins, dict)
            self._cli.append("--host")
            self._cli.append(self._logins["host"])
            self._cli.append("--port")
            self._cli.append(str(self._logins["port"]))
            self._cli.append("--user")
            self._cli.append(self._logins["user"])
            self._cli.append(f"--password={self._logins['password']}")
        self._cli.append("--")

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

    def cluster_status(self) -> None:
        """
        CLuster check method
        """
        _logger.info("Running cluster status check")
        self._cli.append("cluster")
        self._cli.append("status")
        output: dict = self._execute_cli(self._cli)
        _logger.debug(json.dumps(output, indent=2))
        replica: dict = output["defaultReplicaSet"]
        self._cluster_results = {
            "name": output["clusterName"],
            "role": output["clusterRole"],
            "status": replica["status"],
            "topology": replica["topologyMode"],
            "message": replica["statusText"],
        }
        topology = replica["topology"]
        for k, v in topology.items():
            lag = v.get("replicationLagFromImmediateSource")
            primary = MemberRole[v.get("memberRole")].value
            status: str = v.get("status").replace("(", "").replace(")", "")
            r: NodeDict = {
                "node": k.split(":")[0],
                "primary": primary,
                "mode": v.get("mode"),
                "status": status,
                "version": v.get("version"),
                "lag": lag if lag or primary else "00:00:00.000000",
            }
            self._node_results.append(r)
        cluster_status = ClusterReplicaStatus[self._cluster_results["status"]].value
        exit_status = CheckStatus[cluster_status].value
        for s in self._node_results:
            node_status = MemberStatus[s.get("status")].value
            exit_status = max(exit_status, CheckStatus[node_status].value)
        _logger.info("Printing output to stdout and exiting")
        print(tabulate([self._cluster_results], headers="keys"), end="\n\n")
        print(tabulate(self._node_results, headers="keys"))
        sys.exit(exit_status)

    def _get_routers(self) -> int:
        """
        Method to get routers
        """
        _logger.info("Collecting router info")
        cli = self._cli.copy()
        cli.append("clusterset")
        cli.append("list-routers")
        output: dict = self._execute_cli(cli)
        _logger.debug(json.dumps(output, indent=2))
        return len(output["routers"].keys())

    def clusterset_status(self) -> None:
        """
        Method to check clusterset
        """
        _logger.info("Running clusterset check")
        cli = self._cli.copy()
        cli.append("clusterset")
        cli.append("status")
        cli.append("--extended")
        cli.append("1")
        output: dict = self._execute_cli(cli)
        _logger.debug(json.dumps(output, indent=2))
        routers = self._get_routers()
        clusters: dict = output["clusters"]
        set_results: ClustersetDict = {
            "name": output["domainName"],
            "primary_cluster": output["primaryCluster"],
            "primary_server": output["globalPrimaryInstance"],
            "status": output["status"],
            "clusters": len(clusters.keys()),
            "routers": routers,
            "message": output["statusText"],
        }
        for k, v in clusters.items():
            cluster: ClusterDict = {
                "name": k,
                "role": v.get("clusterRole"),
                "status": v.get("status"),
                "globalStatus": v.get("globalStatus"),
                "message": v.get("statusText"),
            }
            self._clusterset_members.append(cluster)
        _logger.info("Printing output to stdout and exiting")
        print(tabulate([set_results], headers="keys"), end="\n\n")
        print(tabulate(self._clusterset_members, headers="keys"))
        clusterset_base_status = ClustersetBaseStatus[set_results["status"]].value
        exit_status = CheckStatus[clusterset_base_status].value
        for s in self._clusterset_members:
            cluster_status = ClustersetStatus[s["status"]].value
            cluster_global_status = ClustersetGlobalStatus[s["globalStatus"]].value
            exit_status = max(
                exit_status,
                CheckStatus[cluster_status].value,
                CheckStatus[cluster_global_status].value,
            )
        sys.exit(exit_status)
