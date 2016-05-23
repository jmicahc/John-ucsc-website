import json
import sys

def svginsubtree(root, iters=[]):
    if 'slice_ids' in root:
        return True
    elif 'children' in root:
        it = iter(root['children'])
        iters.append(it)
        return svginsubtree(next(it), iters=iters)
    else:
        while iters:
            n = next(iters[-1], None)
            if n: return svginsubtree(n, iters=iters)
            iters.pop()
        return False

def deleteNode(node, parent, index, deletes={}):
    if node['id'] == parent['id']:

        Id = node['id']
        if Id in deletes:
            for del_index in deletes[Id]:
                if del_index < index:
                    index -= 1
            deletes[Id].append(index)
        else:
            deletes[Id] = [index]
        del node['children'][index]
    if 'children' in node:
        for child in node['children']:
            deleteNode(child, parent, index)

def trim(root, rootcopy, parents=[], its=[], debug=open('debug.json', 'w')):
    if not svginsubtree(root[1], iters=[]):
        deleteNode(rootcopy, parents[-1], root[0])

    if 'children' in root[1]:
        it = iter(enumerate(root[1]['children']))
        its.append(it)
        parents.append(root[1])
        return trim(next(it), rootcopy, its=its)
    else:
        while its:
            n = next(its[-1], None)
            if n: return trim(n, rootcopy, its=its)
            its.pop()
            parents.pop()

if __name__ == "__main__":
    sys.setrecursionlimit(3000)
    
    f = open('allenwithslice.json', 'r')

    data = json.loads(f.read())
    f = open('allenwithslice.json', 'r')
    copy = json.loads(f.read())

    debug = open('debug.json', 'w')
    trim(tuple([0, data]), copy, debug=debug)

    open('allentrimmed_3.json', 'w').write(json.dumps(copy))
