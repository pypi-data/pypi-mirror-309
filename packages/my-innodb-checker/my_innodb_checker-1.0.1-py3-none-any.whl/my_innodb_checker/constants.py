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
    MISSING = "CRITICAL"


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


class ClustersetBaseStatus(Enum):
    """
    Enum for mysqlsh clusterset base status
    """

    HEALTHY = "OK"
    AVAILABLE = "WARNING"
    UNAVAILABLE = "CRITICAL"


class ClustersetGlobalStatus(Enum):
    """
    Enum for global clusterset status
    """

    OK = "OK"
    OK_NOT_REPLICATING = "WARNING"
    OK_NOT_CONSISTENT = "WARNING"
    OK_MISCONFIGURED = "WARNING"
    NOT_OK = "CRITICAL"
    UNKNOWN = "UNKNOWN"
    INVALIDATED = "CRITICAL"


class ClustersetStatus(Enum):
    """
    Enum for clusterset status
    """

    OK = "OK"
    OK_PARTIAL = "WARNING"
    OK_NO_TOLERANCE = "WARNING"
    OK_NO_TOLERANCE_PARTIAL = "WARNING"
    NO_QUORUM = "CRITICAL"
    OFFLINE = "CRITICAL"
    ERROR = "CRITICAL"
    INVALIDATED = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class ClusterDict(TypedDict, total=False):
    """
    Cluster results dict type
    """

    name: str
    role: str
    status: str
    globalStatus: str
    topology: str
    message: str


class ClustersetDict(TypedDict):
    """
    Clusterset results dict type
    """

    name: str
    primary_cluster: str
    primary_server: str
    status: str
    clusters: int
    routers: int
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
