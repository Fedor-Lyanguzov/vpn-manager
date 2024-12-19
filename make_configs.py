import subprocess

def user_cfg(private_key, n):
    user_cfg = f'''
    [Interface]
    PrivateKey = {private_key}
    Address = 10.0.0.{n}/32
    DNS = 1.1.1.1

    [Peer]
    PublicKey = {public_key}
    AllowedIPs = 0.0.0.0/0, ::/0
    Endpoint = 89.19.211.56:51820
    '''
    return user_cfg

def server_cfg(peers):
    server_cfg = '''
    [Interface]
    PrivateKey = {private_key}
    Address = 10.0.0.1/32
    PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
    ListenPort = 51820

    [Peer]
    PublicKey = {public_key}
    AllowedIPs = 10.0.0.2/32
    '''
    return '\n\n'.join([server_cfg]+list(map(lambda x: peer_cfg(*x), enumerate(peers, 3))))

def peer_cfg(n, peer_public_key):
    peer_cfg = f'''
    [Peer]
    PublicKey = {peer_public_key}
    AllowedIPs = 10.0.0.{n}/32
    '''
    return peer_cfg

peers = []
for n, user in enumerate(['fedor-walker', 'fedor-phone', 'polina-notebook', 'polina-phone'], 3):
    with subprocess.Popen('wg genkey | tee privatekey | wg pubkey > publickey', shell=True):
        pass
    with open('privatekey') as f:
        private_key = f.read().strip()
    with open('publickey') as f:
        public_key = f.read().strip()
    with open(f'{user}.conf', 'w') as f:
        f.write(user_cfg(private_key, n))
    peers.append(public_key)
with open(f'server.conf', 'w') as f:
    f.write(server_cfg(peers))
