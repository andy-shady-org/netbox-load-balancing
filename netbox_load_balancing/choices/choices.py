from utilities.choices import ChoiceSet

__all__ = (
    "HealthMonitorTypeChoices",
    "HealthMonitorHTTPVersionChoices",
    "PoolAlgorythmChoices",
    "PoolSessionPersistenceChoices",
    "PoolBackupSessionPersistenceChoices",
    "ListenerProtocolChoices",
)


class HealthMonitorTypeChoices(ChoiceSet):

    PING = "ping"
    TCP = "tcp"
    HTTP = "http"
    HTTP_ECV = "http-ecv"
    HTTPS_ECV = "https-ecv"
    FTP_ECV = "ftp-ecv"
    UDP_ECV = "udp-ecv"

    CHOICES = [
        (PING, "PING", "green"),
        (TCP, "TCP", "yellow"),
        (HTTP, "HTTP", "blue"),
        (HTTP_ECV, "HTTP-ECV", "cyan"),
        (HTTPS_ECV, "HTTPS-ECV", "orange"),
        (FTP_ECV, "FTP-ECV", "grey"),
        (UDP_ECV, "UDP-ECV", "purple"),
    ]


class HealthMonitorHTTPVersionChoices(ChoiceSet):
    VERSION_1 = "HTTP 1.0"
    VERSION_11 = "HTTP 1.1"

    CHOICES = [
        (VERSION_1, "HTTP 1.0"),
        (VERSION_11, "HTTP 1.1"),
    ]


class PoolAlgorythmChoices(ChoiceSet):
    LEAST_CONNECTION = "least-connection"
    ROUND_ROBIN = "round-robin"
    SOURCE_IP_HASH = "source-ip-hash"

    CHOICES = [
        (LEAST_CONNECTION, "LEAST_CONNECTION", "green"),
        (ROUND_ROBIN, "ROUND_ROBIN", "orange"),
        (SOURCE_IP_HASH, "SOURCE_IP_HASH", "blue"),
    ]


class PoolSessionPersistenceChoices(ChoiceSet):
    NONE = "None"
    SOURCE_IP = "source-ip"
    SSL_BRIDGE = "ssl-bridge"
    COOKIE = "cookie"

    CHOICES = [
        (NONE, "NONE", "green"),
        (SOURCE_IP, "SOURCE_IP", "blue"),
        (SSL_BRIDGE, "SSL_BRIDGE", "orange"),
    ]


class PoolBackupSessionPersistenceChoices(ChoiceSet):
    NONE = "None"
    SOURCE_IP = "source-ip"

    CHOICES = [
        (NONE, "NONE", "red"),
        (SOURCE_IP, "SOURCE_IP", "green"),
    ]


class ListenerProtocolChoices(ChoiceSet):
    TCP = "tcp"
    HTTP = "http"
    UDP = "udp"
    SSL_BRIDGE = "ssl-bridge"

    CHOICES = [
        (TCP, "TCP", "green"),
        (HTTP, "HTTP", "blue"),
        (UDP, "UDP", "cyan"),
        (SSL_BRIDGE, "SSL_BRIDGE", "orange"),
    ]
