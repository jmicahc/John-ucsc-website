import json
import sys

def subtreevolume(root, iters=[], volume=0):
    if 'volume' in root:
        volume += root['volume']
    if 'children' in root and root['children']:
        it = iter(root['children'])
        iters.append(it)
        return subtreevolume(next(it), iters=iters)
    else:
        while iters:
            n = next(iters[-1], None)
            if n: return subtreevolume(n, iters=iters)
            iters.pop()
        return volume


def addvolumes(root, iters=[]):
    print 'adding volume'
    root['size'] = subtreevolume(root, iters=[])
    if 'children' in root and root['children']:
        it = iter(root['children'])
        iters.append(it)
        return addvolumes(next(it), iters=iters)
    else:
        while iters:
            n = next(iters[-1], None)
            if n: return addvolumes(n, iters=iters)
            iters.pop()





if __name__ == "__main__":
    sys.setrecursionlimit(3000)
    
    f = open('allentrimmed_3.json', 'r')

    data = json.loads(f.read())

    debug = open('debug.json', 'w')
    addvolumes(data)

    open('allenwithvolume_4.json', 'w').write(json.dumps(data))
