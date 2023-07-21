import dis

a = ('pen', 'pencil', 'eraser', 'sharpener')


def d():
    return {v: 0 for v in a}


def d2():
    return dict.fromkeys(a, 0)


dis.dis(d2)
print(d2())
