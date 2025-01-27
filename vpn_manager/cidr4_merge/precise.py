from .util import mask, get_data, cidr4_to_node, make_cidr4


def f(x, y):
    t = x
    b = y
    if x[1]>y[1]:
        t = y
        b = x
    ip1, l1, a1 = t
    ip2, l2, a2 = b
    if ip1 & mask[l1] == ip2 & mask[l1]:
        return (0, t)
    t1 = t2 = 0
    while not l1==l2:
        t2 += 2**(32-l2)
        l2 -= 1
        ip2 = ip2 & mask[l2]
    while not ip1 & mask[l1-1] == ip2 & mask[l2-1]:
        t1 += 2**(32-l1)
        l1 -= 1
        ip1 = ip1 & mask[l1]
        t2 += 2**(32-l2)
        l2 -= 1
        ip2 = ip2 & mask[l2]
    r = (ip1 & mask[l1-1], l1-1, a1+a2+t1+t2)
    return (t1+t2, r)
    

def solution(cidrs, M):
    cidrs = sorted((ip, l, 0) for ip, l in cidrs)
    while len(cidrs)>M:
        t = (None, float('+inf'), None)
        for i, (x, y) in enumerate(zip(cidrs, cidrs[1:])):
            m, r = f(x, y)
            if m<t[1]:
                t = (i, m, r)
            if m==0:
                break
        cidrs[t[0]] = t[2]
        del cidrs[t[0]+1]
    s = sum(x[2] for x in cidrs)
    cidrs = [x[:2] for x in cidrs]
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
