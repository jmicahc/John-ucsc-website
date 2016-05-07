from lxml import etree
import glob

if __name__ == "__main__":
    files = glob.glob('1*')
    for fname in files[1:]:
        xml = etree.XML(open(fname).read())
        xml.set('viewBox', "0 0 " + xml.get('width') + " " + xml.get('height'))
        xml.attrib.pop('width')
        xml.attrib.pop('height')
        print xml.keys(), xml.get('viewBox'), fname
        et = etree.ElementTree(xml)
        et.write(fname)

