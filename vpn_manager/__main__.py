from dataclasses import dataclass
from textwrap import dedent


@dataclass
class Peer:
    public_key: str
    private_key: str
    address_cidr: str
    port: str
    endpoint: str = None


def format_static_peer(static_peer, routes, keepalive=30):
    return f"""
[Peer]
PublicKey = {static_peer.public_key}
AllowedIPs = {routes}
Endpoint = {static_peer.endpoint}:{static_peer.port}
PersistentKeepAlive = {keepalive}
""".strip()


def format_interface(peer, dns, forward=False):
    if forward:
        forward = dedent(
            """\
            PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
            PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
            """
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
    return f"""
[Interface]
PrivateKey = {peer.private_key}
Address = {peer.address_cidr}
{port}\
{dns}\
{forward}\
""".strip()


def remove_empty_lines(text):
    return "\n".join([s for s in text.splitlines() if s.strip()])


def main():
    print("run")


if __name__ == "__main__":
    main()
