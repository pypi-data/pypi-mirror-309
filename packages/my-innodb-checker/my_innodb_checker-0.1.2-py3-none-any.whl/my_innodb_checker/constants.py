"""
Constants module
"""

from enum import Enum
from typing import TypedDict


class CheckStatus(Enum):
    """
    Enum for nagios exit codes
    """

    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOW = 3


class MemberStatus(Enum):
    """
    Enum for member status
    """

    ONLINE = "OK"
    RECOVERING = "WARNING"
    OFFLINE = "CRITICAL"
    ERROR = "CRITICAL"
    UNREACHABLE = "UNKNOW"
    (MISSING) = "CRITICAL"


class MemberRole(Enum):
    """
    Enum for member role
    """

    PRIMARY = True
    SECONDARY = False


class ClusterReplicaStatus(Enum):
    """
    Enum for Mysql innodb cluster status
    """

    OK = "OK"
    OK_PARTIAL = "OK"
    OK_NO_TOLERANCE = "WARNING"
    OK_NO_TOLERANCE_PARTIAL = "WARNING"
    NO_QUORUM = "CRITICAL"
    OFFLINE = "CRITICAL"
    ERROR = "CRITICAL"
    UNREACHABLE = "CRITICAL"
    UNKNOWN = "UNKNOW"
    FENCED_WRITES = "WARNING"


class ClusterDict(TypedDict, total=False):
    """
    Cluster results dict type
    """

    name: str
    role: str
    status: str
    topology: str
    message: str


class NodeDict(TypedDict):
    """
    Node results dict type
    """

    node: str
    primary: bool
    mode: str
    status: str
    version: str
    lag: str


class MyLogin(TypedDict):
    """
    Mysql login dictionary
    """

    user: str
    password: str
    host: str
    port: str
