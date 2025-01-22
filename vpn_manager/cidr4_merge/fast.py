from heapq import heapify, heappush, heappop
from .util import mask, get_data, cidr4_to_node, make_cidr4


def solution(cidrs, M):
    h = []
    d = {}
    for ip, l in cidrs:
        h.append((32-l, ip, l))
        d[(ip, l)] = 0
    heapify(h)
    while len(h)>M:
        x1, ip1, l1 = heappop(h)
        x2, ip2, l2 = h[0]
        if l1==l2 and ip1 & mask[l1-1] == ip2 & mask[l2-1]:
            heappop(h)
            if (ip1 & mask[l1-1], l1-1) not in d:
                heappush(h, (x1+1, ip1 & mask[l1-1], l1-1))
                d[(ip1 & mask[l1-1], l1-1)] = d[(ip1, l1)] + d[(ip2, l2)]
            del d[(ip2, l2)]
        else:
            if (ip1 & mask[l1-1], l1-1) not in d:
                heappush(h, (x1+1, ip1 & mask[l1-1], l1-1))
                d[(ip1 & mask[l1-1], l1-1)] = d[(ip1, l1)] + 2**x1
        del d[(ip1, l1)]
        s = sum(d.values())
        cidrs = list(d.keys())
    return cidrs, s


def main():
    M = 20
    a = get_data()
    b = list(map(cidr4_to_node, a))
    cidrs, s = solution(b, M)
    cidrs = sorted([make_cidr4(*x) for x in cidrs])
    print(cidrs, s, sep='\n')
    

if __name__=='__main__':
    import cProfile
    main()
            
