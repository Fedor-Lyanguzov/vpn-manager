from dataclasses import dataclass


@dataclass
class Peer:
    public_key: str
    private_key: str
    address_cidr: str
    port: str
    endpoint: str = None


def format_static_peer(static_peer, routes, keepalive=30):
    return (
        "[Peer]\n"
        f"PublicKey = {static_peer.public_key}\n"
        f"AllowedIPs = {routes}\n"
        f"Endpoint = {static_peer.endpoint}:{static_peer.port}\n"
        f"PersistentKeepAlive = {keepalive}\n"
    ).strip()


def format_interface(peer, dns, forward=False):
    if forward:
        forward = (
            "PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE\n"
            "PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE\n"
        )
        # wg0 always?
        # eth0 always?
    else:
        forward = ""
    if peer.port:
        port = f"ListenPort = {peer.port}\n"
    else:
        port = ""
    dns = f"DNS = {dns}\n"
    return (
        "[Interface]\n"
        f"PrivateKey = {peer.private_key}\n"
        f"Address = {peer.address_cidr}\n"
        f"{port}"
        f"{dns}"
        f"{forward}"
    ).strip()
