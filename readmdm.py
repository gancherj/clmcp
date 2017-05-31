import xml.etree.ElementTree as ET
import sys

class MDM:
    pass

def read_mdm(filename):
    mdmroot = ET.parse(filename).getroot()
    seriesname = mdmroot.find('SeriesName').text
    namespace = mdmroot.find('Namespace').text
    version = mdmroot.find('Version').text
    enums = mdmroot.find('EnumList').findall('Enum')
    structs = mdmroot.find('StructList').findall('Struct')
    mdm = MDM()
    mdm.seriesname = seriesname
    mdm.namespace = namespace
    mdm.version = version
    mdm.enums = enums
    mdm.structs = structs
    return mdm

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("no mdm given")
        sys.exit()
    else:
        mdm = read_mdm(sys.argv[1])
