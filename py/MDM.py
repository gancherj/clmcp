import re, struct as struc
import xml.etree.ElementTree as ET

class TypeInfo:
    basetypes = {
        'byte': 'uint8_t',
        'char': 'char',
        'bool': 'bool',
        'int16': 'int16_t',
        'uint16': 'uint16_t',
        'int32': 'int32_t',
        'uint32': 'uint32_t',
        'int64': 'int64_t',
        'real32': 'float',
        'real64': 'double',
        'string': 'char'}

    basetypes_i = { # basetypes but only ints
        'byte': 'uint8_t',
        'char': 'char',
        'bool': 'bool',
        'int16': 'int16_t',
        'uint16': 'uint16_t',
        'int32': 'int32_t',
        'uint32': 'uint32_t',
        'int64': 'int64_t',
        'real32': 'uint32_t',
        'real64': 'uint64_t',
        'string': 'char'}

    def __init__(self, typestr): #-1 and true -> varying array
        underlying = re.search('[a-zA-Z]+[0-9]*', typestr).group(0)
        arrayparam = re.search('\[[0-9]*\]', typestr)
        if arrayparam is not None:
            arrayparam = arrayparam.group(0)
            if arrayparam != '[]':
                size = re.search(r'[0-9]+', arrayparam).group(0)
                self.isarray = True
                self.arraysize = size
                self.typename = underlying
            else:
                self.isarray = True
                self.arraysize = "-1"
                self.typename = underlying
        else:
            self.isarray = False
            self.arraysize = ""
            self.typename = underlying
        self.islargearray = False 

        if underlying == "string" and self.isarray:
            print("Arrays of strings not supported directly; put string in a struct and do array of struct")
        elif underlying == "string" and not self.isarray: # strings are arrays of chars
            self.isarray = True
            self.arraysize = "-1"
            self.typename = "char"

    
class FieldInfo:
    #typeinfo
    #units
    #name
    def __init__(self, f):
        self.typeinfo = TypeInfo(f.attrib['Type'])
        self.name = f.attrib['Name']
        if 'Units' in f.attrib:
            self.units = f.attrib['Units']
        else:
            self.units = None
        if 'LargeArray' in f.attrib:
            self.typeinfo.islargearray = True

    def emit(self):
        fieldstr = ""
        if self.units is not None:
            fieldstr += "// Units: " + self.units + " \n"
        if self.typeinfo.typename in TypeInfo.basetypes:
            underlying = TypeInfo.basetypes[self.typeinfo.typename]
        else:
            underlying = self.typeinfo.typename
        if self.typeinfo.isarray:
            underlying += "*"
        fieldstr += underlying + " " + self.name + ";\n"
        if self.typeinfo.isarray:
            fieldstr += "array_info " + self.name + "_ai;\n"
        return fieldstr

class StructInfo:
    def __init__(self, mdm, struct):
        self.name = struct.attrib['Name']
        self.seriesname = (mdm.seriesname+"\0\0\0\0\0\0\0\0")[:8]
        self.version = mdm.version
        if 'Extends' in struct.attrib:
            self.parent = struct.attrib['Extends']
        else:
            self.parent = 'lmcp_object'
        if 'Series' not in struct.attrib:
            self.parentseries = mdm.seriesname
        else:
            self.parentseries = struct.attrib['Series']
        self.parentserieslong = struc.unpack(">Q", (str.encode(self.parentseries) + b'\0\0\0\0\0\0\0\0')[:8])
        self.fields = [FieldInfo(f) for f in struct]
        self.subscription = re.compile("/").sub(".", mdm.namespace) + '.' + self.name
        #self.id created by mdm
    
    def emit(self):

        struct_header = "typedef struct {"
        struct_footer = "}" + self.name + ";"
        parent_field = self.parent + " super;"
        return '\n'.join([
            "#define LMCP_"+self.name+"_SUB \""+self.subscription+"\"\n",
            "#define LMCP_"+self.name+"_TYPENAME \""+self.name+"\"\n",
            struct_header,
            parent_field]
            + [f.emit() for f in self.fields]
            + [struct_footer])

class EnumInfo:
    def __init__(self, enum):
        self.name = enum.attrib['Name']
        vs = {}
        for entry in enum.findall('Entry'):
            if 'Value' in entry.attrib:
                vs[entry.attrib['Name']] = entry.attrib['Value']
            else:
                vs[entry.attrib['Name']] = None
        self.values = vs


    def emit(self):
        enum_header = "typedef enum {"
        enum_footer = "} " + self.name + ";"
        
        values = []
        for vn in self.values:
            if self.values[vn] is not None:
                values += [vn +" = "+self.values[vn] + ","]
            else:
                values += [vn + ","]
        
        return '\n'.join([
            enum_header]
            + values
            + [enum_footer])

class MDM:
    def __init__(self, filename):
        mdmroot = ET.parse(filename).getroot()
        seriesname = mdmroot.find('SeriesName')
        if seriesname is not None:
            seriesname = seriesname.text
        else:
            seriesname = ""

        namespace = mdmroot.find('Namespace')
        if namespace is not None:
            namespace = namespace.text
        else:
            namespace = ""


        version = mdmroot.find('Version')
        if version is not None:
            version = version.text
        else:
            version = ""

        enums = mdmroot.find('EnumList')
        if enums is not None:
            enums = enums.findall('Enum')
        else:
            enums = []

        structs = mdmroot.find('StructList')
        if structs is not None:
            structs = structs.findall('Struct')
        else:
            structs = []

        self.seriesname = seriesname
        self.namespace = namespace
        self.version = version
        self.enums = [EnumInfo(e) for e in enums]
        self.structs = [StructInfo(self, s) for s in structs]
        for i in range(len(self.structs)):
            self.structs[i].id = str(1+i)
        self.seriesnamelong = struc.unpack(">Q", (str.encode(seriesname) + b'\0\0\0\0\0\0\0\0')[:8])


    def emit(self):
        header = ""
        for struct in self.structs:
            header += struct.emit()
        for enum in self.enums:
            header += enum.emit()
        return header 
