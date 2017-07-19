import re, struct as struc
import xml.etree.ElementTree as ET

class TypeInfo:
    basetypes = {
        'byte': 'uint8_t',
        'char': 'char',
        'bool': 'uint8_t',
        'int16': 'int16_t',
        'uint16': 'uint16_t',
        'int32': 'int32_t',
        'uint32': 'uint32_t',
        'int64': 'int64_t',
        'real32': 'float',
        'real64': 'double',
        'string': 'char'}


    def __init__(self, typestr): #-1 and true -> varying array
        underlying = re.search('[a-zA-Z]+[0-9]*[a-zA-Z]*', typestr).group(0)
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
            print("ERROR: Arrays of strings not supported directly; put string in a struct and do array of struct")
        elif underlying == "string" and not self.isarray: # strings are arrays of chars
            self.isarray = True
            self.arraysize = "-1"
            self.typename = "char"

    
class FieldInfo:
    #typeinfo
    #units
    #name
    #kind
    #typeid
    #version
    #series
    def fillkind(self, mdm):
        if self.typeinfo.typename in TypeInfo.basetypes:
            self.kind = 'base'
        elif mdm.is_struct(self.typeinfo.typename):
            self.kind = 'struct'
        elif mdm.is_enum(self.typeinfo.typename):
            self.kind = 'enum'
        else:
            print ("ERROR: weird kind: " + self.typeinfo.typename)
            self.kind = 'unknown'

        if self.kind == 'struct':
            struct = mdm.get_struct(self.typeinfo.typename)
            self.seriesname = struct.seriesname
            self.id = struct.id
            self.version = struct.version

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
        if self.kind == 'base':
            underlying = TypeInfo.basetypes[self.typeinfo.typename]
        elif self.kind == 'struct':
            underlying = self.typeinfo.typename + "*"
        elif self.kind == 'enum':
            underlying = self.typeinfo.typename
        else:
            print ("ERROR: weird kind: " + self.kind)
        if self.typeinfo.isarray:
            underlying += "*"
        fieldstr += underlying + " " + self.name + ";\n"
        if self.typeinfo.isarray:
            fieldstr += "array_info " + self.name + "_ai;\n"
        return fieldstr

class StructInfo:
    def __init__(self, mdm, struct):
        self.name = struct.attrib['Name']
        self.seriesname = mdm.seriesname
        self.version = mdm.version
        self.mdm = mdm
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

    def fillkinds(self,mdm):
        for field in self.fields:
            field.fillkind(mdm)
    
    def emit(self):

        struct_header = "typedef struct {"
        struct_footer = "}" + self.name + ";"
        if self.parent == 'lmcp_object':
            parent_field = self.parent + " super;"
        else:
            parent_field = self.parent + " super;"
        return '\n'.join([
            "#define LMCP_"+self.name+"_SUB \""+self.subscription+"\"\n",
            "#define LMCP_"+self.name+"_TYPENAME \""+self.name+"\"\n",
            struct_header,
            parent_field]
            + [f.emit() for f in self.fields]
            + [struct_footer])
    
    def deps(self):
        out = []
        seen_enum = False
        for field in self.fields:
            if field.kind == 'struct':
                out += [field.typeinfo.typename]
            elif field.kind == 'enum' and not seen_enum:
                out += ['enums']
                seen_enum = True
        return out


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
                values += [self.name+"_"+vn +" = "+self.values[vn] + ","]
            else:
                values += [self.name+"_"+vn + ","]
        
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
        for i in range(len(self.structs)):
            self.structs[i].fillkinds(self)

        self.seriesnamelong = struc.unpack(">Q", (str.encode(seriesname) + b'\0\0\0\0\0\0\0\0')[:8])


    def emit(self):
        header = ""
        for struct in self.structs:
            header += struct.emit()
        for enum in self.enums:
            header += enum.emit()
        return header 

    def is_struct(self,name):
        for struct in self.structs:
            if struct.name == name:
                return True
    
    def get_struct(self, name):
        for struct in self.structs:
            if struct.name == name:
                return struct

    def is_enum(self, name):
        for enum in self.enums:
            if enum.name == name:
                return True
