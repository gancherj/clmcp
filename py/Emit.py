import re

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
        'string': 'char*'}

    def __init__(self, isarray, arraysize, typename):
        self.isarray = isarray
        self.arraysize = arraysize
        self.typename = typename
    

def parse_type(typestr):
    underlying = re.search('[a-zA-Z]+[0-9]*', typestr).group(0)
    arrayparam = re.search('\[[0-9]*\]', typestr)
    if arrayparam is not None:
        arrayparam = arrayparam.group(0)
        if arrayparam != '[]':
            size = re.search(r'[0-9]+', arrayparam).group(0)
            return TypeInfo(True, size, underlying)
        else:
            return TypeInfo(True, "-1", underlying)
    else:
        return TypeInfo(False, "", underlying)
    

def emit_field(field):
    typeinfo = parse_type(field.attrib['Type'])
    fieldstr = ""
    if 'Units' in field.attrib:
        fieldstr += "// Units: " + field.attrib['Units'] + "\n"

    if typeinfo.typename in TypeInfo.basetypes:
        underlying = TypeInfo.basetypes[typeinfo.typename]
    else:
        underlying = typeinfo.typename

    if typeinfo.isarray:
        underlying += "*"
    
    fieldstr += underlying + " " + field.attrib['Name'] + ";\n"
    if typeinfo.isarray:
        fieldstr += "array_info " + field.attrib['Name']+"_ai;\n"
    return fieldstr

def emit_structdef(struct):
    if 'Extends' in struct.attrib:
        parent = struct.attrib['Extends']
    else:
        parent = 'lmcp_object'


    struct_header = "typedef struct {"
    struct_footer = "} " + struct.attrib['Name'] + ";"

    parent_field = parent + " super;"

    return '\n'.join([
        struct_header,
        parent_field] 
        + [emit_field(field) for field in struct]
        + [struct_footer])
   
def emit_enumvalue(value):
    if 'Value' in value.attrib:
        return value.attrib['Name']+" = "+value.attrib['Value']+","
    else:
        return value.attrib['Name']+","

def emit_enumdef(enum):
    enum_header = "typedef enum {"
    enum_footer = "} " + enum.attrib['Name'] + ";"

    return '\n'.join([
        enum_header]
        + [emit_enumvalue(value) for value in enum.findall('Entry')]
        + [enum_footer])
