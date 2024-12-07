#!/usr/bin/env python3
import argparse
import xml.dom.minidom
import lxml.etree as ET
import pynmrstar
import sys
from collections import defaultdict

from pynmrstar import Entry,Saveframe, Loop
from xml.etree.ElementTree import Element

class _SaveframeWrapper:


    def __init__(self, sf:pynmrstar.Saveframe):
        self.saveframe = sf
        self.tagcounter = defaultdict(int)
        self.tagindexer = defaultdict(int)
        self.preprocess = True

    def add_tag(self,key:str,value:str):
        """index or add_tag, depending self.preprocess"""
        if self.preprocess:
            self.tagcounter[key] += 1
        else:
            kname = key;
            if self.tagcounter[key] > 1:
                kname = key + str(self.tagindexer[key])
                self.tagindexer[key] += 1
            self.saveframe.add_tag(kname,value)


class NMRStarXml:
    """Bidirectional conversion of NMRStar to and from XML"""
    _TAG_TOKEN = "metadata"
    _LOOP_TOKEN = "table"
    _CATEGORY_TOKEN = "category"
    _COLUMN_TOKEN = "column"
    _DATA_TOKEN = "data"
    _ORIGIN_ATTRIB = "origin"
    _NMRSTAR = "NMR-STAR"
    """Value for NMR-STAR origin"""
    _LIST_SEPARATORS=':.#,-!@#$%^&*'


    def __init__(self):
        self.source = False
        self.used_namespaces = set( )
        self.tag_ns_map = {}


    def star_entry(self,entry:pynmrstar.Entry)->Element:
        """Convert Entry to XML Element"""
        root = ET.Element(entry.entry_id)
        root.attrib[self._ORIGIN_ATTRIB] = self._NMRSTAR
        tree = ET.ElementTree(root)
        for s in entry:
            #print(s)
            root.append(self.star_savefame(s))
        return tree

    def _ns_name(self,name):
        assert getattr(self,'reverse_nsmap') != None
        try:
            qname = ET.QName(name)
            lname = qname.localname
        except:
            print(name)
            raise
        if qname.namespace == None:
            return lname
        ns = self.reverse_nsmap[qname.namespace]
        self.used_namespaces.add(qname.namespace)
        existing = self.tag_ns_map.get(lname)
        if existing:
            if existing != ns:
                raise ValueError("Duplicate namespaces {} and {} for tag {}".format(ns,existing,lname))
        else:
            self.tag_ns_map[lname] = ns
        #return "{}-{}".format(ns,qname.localname)
        return lname

    def xml_entry(self, root:Element)->pynmrstar.Entry:
        """Convert XML Element to Entry"""
        a = root.attrib.get(self._ORIGIN_ATTRIB)
        if a == self._NMRSTAR:
            return self._xml_entry_starorigin(root)

        self.reverse_nsmap = {}

        for k,v in root.nsmap.items( ):
            self.reverse_nsmap[v] = k


        flc_counts = defaultdict(int)
        flc_counter = defaultdict(int)
        rname = self._ns_name(root.tag)
        prefix = ET.QName(root.tag).localname
        entry = Entry.from_scratch(rname)
        for c in root:
            flc_counts[c.tag] += 1

        for c in root:
            name = self._ns_name(c.tag)
            if flc_counts[c.tag] > 1:
                name += str(flc_counter[c.tag])
                flc_counter[c.tag] += 1
            sf = self._xml_flatten_to_saveframe(c,name, prefix)
            entry.add_saveframe(sf)


        if self.tag_ns_map:
            sf = Saveframe.from_scratch('namespace_map', tag_prefix='map')
            for k in sorted(self.tag_ns_map.keys()):
                v = self.tag_ns_map[k]
                sf.add_tag(k,v)
            self._insert_saveframe(entry,sf)

        if self.used_namespaces:
            sf = Saveframe.from_scratch('namespaces', tag_prefix='ns')
            for url in self.used_namespaces:
                short = self.reverse_nsmap[url]
                sf.add_tag(short,url)
            self._insert_saveframe(entry,sf)

        return entry

    def _insert_saveframe(self,entry:pynmrstar.Entry,saveframe:pynmrstar.Saveframe):
        """add saveframe to beginning of list"""
        entry.add_saveframe(saveframe) #use validation checks
        last = entry.frame_list.pop()
        assert last == saveframe
        entry.frame_list.insert(0,last)

    def _xml_entry_starorigin(self, root:Element)->pynmrstar.Entry:
        """Convert XML Element that was convert from NMR-STAR back to Entry"""
        assert root.attrib.get(self._ORIGIN_ATTRIB) == self._NMRSTAR
        entry = Entry.from_scratch(root.tag)

        for c in root:
            sf = self.xml_saveframe(c)
            entry.add_saveframe(sf)

        return entry


    def star_savefame(self,sf:Saveframe)->Element:
        """Convert saveframe to XML Element"""
        e = ET.Element(sf.name)
        if self.source:
            e.attrib['source'] = sf.source
        e.attrib[self._CATEGORY_TOKEN] = sf.category
        if sf.tag_prefix:
            e.attrib['prefix'] = sf.tag_prefix[1:]
        tags = [t for t in sf.tag_iterator()]
        if tags:
            md = ET.SubElement(e,self._TAG_TOKEN)
            for tag in tags:
                te = ET.SubElement(md,tag[0])
                te.text = tag[1]

        for loop in sf.loop_iterator():
            lp = ET.SubElement(e,self._LOOP_TOKEN)
            lp.attrib[self._CATEGORY_TOKEN] = loop.category[1:]
            dlength = len(loop.category) + 1 #+1 for . separator
            for c in loop.get_tag_names( ):
                celem = ET.SubElement(lp,self._COLUMN_TOKEN)
                celem.text = c[dlength:]
            for d in loop:
                celem = self.listpack(d)
                lp.append(celem)

        return e

    def xml_saveframe(self, flc:Element)->Saveframe:
        """Convert XML Element to Saveframe
        :param flc: first level child
        """
        prefix = flc.get('prefix')
        if prefix:
            p = self.startoken(prefix)
            outf = Saveframe.from_scratch(flc.tag, tag_prefix=p, source=flc.attrib.get('source'))
        else:
            outf = Saveframe.from_scratch(flc.tag, source=flc.attrib.get('source'))
        for m in flc.findall(self._TAG_TOKEN):
            for c in m:
                outf.add_tag(c.tag,c.text)
        for t in flc.findall(self._LOOP_TOKEN):
            cat = t.attrib[self._CATEGORY_TOKEN]
            prefix = self.startoken(cat) + '.'
            lp = Loop.from_scratch(category=cat)
            for col in t.findall(self._COLUMN_TOKEN):
                lp.add_tag(prefix + col.text)
            for row in t.findall(self._DATA_TOKEN):
                lst = self.listunpack(row)
                lp.add_data(lst)
            outf.add_loop(lp)

        return outf

    def _clean_tag_name(self,tag:str)->str:
        """Cleanup string to be valid tag"""
        n = self._ns_name(tag)
        return n.replace('.','-')

    def _xml_flatten_to_saveframe(self, flc:Element,name:str,prefix:str)->Saveframe:
        """Convert XML Element to Saveframe by flattening
        :param flc: first level child
        """
        outf = Saveframe.from_scratch(name,tag_prefix=prefix)
        wrapper = _SaveframeWrapper(outf)
        self._recurse_xml(wrapper,flc,'')
        wrapper.preprocess = False
        self._recurse_xml(wrapper,flc,'')
        return outf

    def _recurse_xml(self,sw:_SaveframeWrapper,element:Element,parentpath:str)->None:
        n = str(element.tag)
        path = parentpath + self._ns_name(n)
        for k, v in element.attrib.items():
            cleank = self._clean_tag_name(k)
            sw.add_tag(path + "attr_" + cleank,v)
        text = element.text.strip( ) if element.text else None
        if text:
            sw.add_tag(path, text)
        for c in element:
            self._recurse_xml(sw,c,path + '-')


    def startoken(self,name):
        #type (self,name:str)->str:
        """Convert XML token to NMRstar convention (add _ prefix)"""
        return '_' + name

    def listpack(self,lst:list)->Element:
        """pack a list into XML Element; use space by default,
        otherwise record separator used"""
        e = ET.Element(self._DATA_TOKEN)
        if not any(s for s in lst if ' ' in s):
            e.text = ' '.join(lst)
            return e
        for sep in self._LIST_SEPARATORS:
            if not any(s for s in lst if sep in s):
                e.text = sep.join(lst)
                e.attrib["separator"] = sep
            return e
        raise ValueError("Unable to find separator in {} for list {}".format(self._LIST_SEPARATORS,lst))

    def listunpack(self,packed:Element)->list:
        """Convert an XML Element generated by listpack
        back into original list"""
        sep = packed.attrib.get("separator")
        sep = sep if sep != None else ' '
        lst = packed.text.split(sep)
        return lst

class Translator:
    """Translate to and from NMRStar <-> XML"""

    def __init__(self,infile,outfile):
        self.infile = infile
        self.outfile = outfile
        self.ns = NMRStarXml( )
        self.PY3 = (sys.version_info[0] == 3)

    def __enter__(self):
        if self.outfile:
            self.dest = open(self.outfile,'w')
        else:
            self.dest = sys.stdout
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dest.close()

    def translate_star(self,e:Entry)->None:
        xd = self.ns.star_entry(e)
        root = xd.getroot()
        if self.PY3:
            s = ET.tostring(root, encoding='unicode')
        else:
            s = ET.tostring(root)
        dom = xml.dom.minidom.parseString(s)
        print(dom.toprettyxml(),file=self.dest)

    def translate_xml(self,x:bytes)->None:
        parser = ET.XMLParser(remove_comments=True)
        xmldom = ET.fromstring(x,parser)
        orig = xmldom.attrib.get('original')
        ne = self.ns.xml_entry(xmldom)
        print(ne,file=self.dest)


    def _translate_star_to_xml(self, datain:str)->None:
        try:
            entry = Entry.from_string(datain)
            self.translate_star(entry)
            return
        except Exception as exc:
            source = self.infile if self.infile else "stdin"

            print("{} not NMR-STAR: {}".format(source,exc),file=sys.stderr)

    def _translate_xml_to_star(self, datain:bytes):
        try:
            self.translate_xml(datain)
            return
        except Exception as exc:
            source = self.infile if self.infile else "stdin"
            print("{} not      XML: {}".format(source,exc),file=sys.stderr)
            raise

    def star_translate(self):
        """perform translation based on constructor arguments"""
        if self.infile:
            with open(self.infile) as f:
                inputdata = f.read()
        else:
            inputdata = sys.stdin.read()
        self._translate_star_to_xml(inputdata)

    def xml_translate(self):
        """perform translation based on constructor arguments"""
        if self.infile:
            with open(self.infile,"rb") as f:
                inputdata = f.read()
        else:
            inputdata = sys.stdin.read().encode( )
        self._translate_xml_to_star(inputdata)


def starxml( ):
    parser = argparse.ArgumentParser(description="Translate NMR-STAR file to XML" )
    parser.add_argument('-i','--input',help="NMR-STAR input file (default stdin)")
    parser.add_argument('-o','--output',help="XML output file (default stdout)")
    parser.add_argument('--starxml',action='store_true',help=argparse.SUPPRESS) #only used for test call
    args = parser.parse_args()
    with Translator(args.input,args.output) as tr:
        tr.star_translate()

def xmlstar( ):
    parser = argparse.ArgumentParser(description="Translate XML file to NMR-STAR" )
    parser.add_argument('-i','--input',help="XML input file (default stdin)")
    parser.add_argument('-o','--output',help="NMR-STAR output file (default stdout)")
    parser.add_argument('--xmlstar',action='store_true',help=argparse.SUPPRESS) #only used for test call
    args = parser.parse_args()
    with Translator(args.input,args.output) as tr:
        tr.xml_translate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test frame (bypass setup.py console_scripts")
    grp =  parser.add_mutually_exclusive_group(required=True)
    grp.add_argument("--starxml",action='store_true')
    grp.add_argument("--xmlstar",action='store_true')
    args, _ = parser.parse_known_args()
    if args.starxml:
        starxml()
    if args.xmlstar:
        xmlstar()






