from lxml import etree
import glob

if __name__ == "__main__":
    files = glob.glob('1*')
    for i, fname in enumerate(files):
        xml = etree.XML(open(fname).read())
        xml.set('id', 'slice-' + str(i))
        xml.set('class', 'brain-slice')
        print xml.keys(), xml.get('viewBox'), fname
        et = etree.ElementTree(xml)
        et.write(fname)

