from vpn_manager.peers import *

def test_format_static_peer():
    sp = Peer('PUB', "PRV", '10.0.0.1/32', '12345', '127.0.0.1')
    peer_section = format_static_peer(sp, '0.0.0.0/0')
    assert peer_section == '[Peer]\nPublicKey = PUB\nAllowedIPs = 0.0.0.0/0\nEndpoint = 127.0.0.1:12345\nPersistentKeepAlive = 30'


def test_true():
    assert format_interface(Peer('PUB', 'PRV', '10.0.0.1/32', 'PORT'), '1.1.1.1') \
        == '[Interface]\nPrivateKey = PRV\nAddress = 10.0.0.1/32\nListenPort = PORT\nDNS = 1.1.1.1'
    assert format_interface(Peer('PUB', 'PRV', '10.0.0.1/32', None), '1.1.1.1') \
        == '[Interface]\nPrivateKey = PRV\nAddress = 10.0.0.1/32\nDNS = 1.1.1.1'
    assert format_interface(Peer('PUB', 'PRV', '10.0.0.1/32', 'PORT'), '1.1.1.1', forward=True) \
        == '[Interface]\nPrivateKey = PRV\nAddress = 10.0.0.1/32\nListenPort = PORT\nDNS = 1.1.1.1\nPostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE\nPostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE'
    assert format_interface(Peer('PUB', 'PRV', '10.0.0.1/32', None), '1.1.1.1', forward=True) \
        == '[Interface]\nPrivateKey = PRV\nAddress = 10.0.0.1/32\nDNS = 1.1.1.1\nPostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE\nPostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE'

