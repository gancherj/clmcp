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

def emit_struct(struct, filename, templ, series, namesp, version):
    return (templ + "-D version=" + version + "-D namespace="+namesp+" -D series="+series+" -D mdm="+filename+" -D struct="+struct.attrib['Name']+"-o "+struct.attrib['Name']+".c")

def emit_struct(enum, filename, templ):
    return (templ + "-D version=" + version + "-D namespace="+namesp+" -D series="+series+" -D mdm="+filename+" -D enum="+enum.attrib['Name']+"-o "+enum.attrib['Name']+".c")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: " + sys.argv[0] + " in.mdm struct_templ.c enum_templ.c")
        sys.exit()
    else:
        mdm = read_mdm(sys.argv[1])
        
