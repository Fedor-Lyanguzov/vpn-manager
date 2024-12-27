from dataclasses import dataclass

@dataclass
class StaticPeer:
    public_key: str
    endpoint: str
    port: str


def format_static_peer(static_peer, routes, keepalive=30):
    return f'''[Peer]
PublicKey = {static_peer.public_key}
AllowedIPs = {routes}
Endpoint = {static_peer.endpoint}:{static_peer.port}
PersistentKeepAlive = {keepalive}'''
    


def main():
    print("run")


if __name__ == "__main__":
    main()
