import json


def svginsubtree(root):
  if 'path_ids' in root:
      return True



  if 'children' in root:
      for child in root['children']:
          return svginsubtree(child)

def trim(root, parent=None, index=-1):
    if not svginsubtree(root):
        del parent['children'][index]

    if 'children' in root:
        for i, child in enumerate(root['children']):
            trim(child, parent=root, index=i)

if __name__ == "__main__":
    f = open('allenwithslice.json', 'r')

    data = json.loads(f.read())

    trim(data)

    open('allentrimmed_3.json', 'w').write(json.dumps(data))
