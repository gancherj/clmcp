from MDM import *

# emit_sizecalc: structinfo -> string
# emit_structpack: structinfo -> string
# emit_structunpack: structinfo -> string


class Emits:
    struct_methods = {}
    struct_headers = {}
    toplevel_methods = {}
    toplevel_headers = {}
    @staticmethod
    def header_filename(struct):
        return struct.name+".h"
    @staticmethod
    def c_filename(struct):
        return struct.name+".c"
    @staticmethod
    def emit_header_top(struct):
        s = '''
#pragma once
#include <stdlib.h>
#include <inttypes.h>
#include <string.h>
#include "common/struct_defines.h"
#include "common/conv.h"
'''
        if struct.parent != 'lmcp_object':
            s += '#include \"'+struct.parent+'.h\"\n'
        for dep in struct.deps():
            s += '#include \"'+dep+'.h\"\n'

        return s
    @staticmethod
    def emit_struct_header(struct):
        s = ""
        for h in Emits.struct_headers:
            s += (Emits.struct_headers[h])(struct)
        return s
    @staticmethod
    def emit_c(struct):
        s = ""
        s += '''
#include <stdlib.h>
#include <inttypes.h>
#include "common/struct_defines.h"
#include "common/conv.h"
'''
        s += '#include \"'+struct.name+'.h\"\n'
        if struct.parent != 'lmcp_object':
            s += '#include \"'+struct.parent+'.h\"\n'
        for dep in struct.deps():
            s += '#include \"'+dep+'.h\"\n'
        for m in Emits.struct_methods:
            s += (Emits.struct_methods[m])(struct)
        return s

    @staticmethod
    def emit_struct_switch(mdm, cases, var, defaultcase): #cases is a dict from struct names to strings (code to do in that case)
        s = ""
        s += "switch (" + var + ") { \n"
        for struct in mdm.structs:
            s += "case "+str(struct.id)+":\n"
            s += cases[struct.name] + "\n"
            s += "break; \n"
        s += "default: \n" + defaultcase + "\n"
        s += "} \n"
        return s
    
    @staticmethod
    def emit_toplevel_c(mdm):
        s = "#include \"common/struct_defines.h\"\n"
        for struct in mdm.structs:
            s += '#include \"'+struct.name+'.h\"\n'
        for mname in Emits.toplevel_methods:
            s += (Emits.toplevel_methods[mname])(mdm)
        return s

    @staticmethod
    def emit_toplevel_header(mdm):
        s = "#pragma once\n"
        s += "#include \"common/struct_defines.h\"\n"
        for struct in mdm.structs:
            s += '#include \"'+struct.name+'.h\"\n'
        for mname in Emits.toplevel_methods:
            s += (Emits.toplevel_headers[mname])
        return s

def emit_toplevel_packsize(mdm):
    s = "uint32_t lmcp_packsize(lmcp_object* o) { \n"
    cases = {struct.name : "return lmcp_packsize_"+struct.name+"(("+struct.name+"*)o);\n" for struct in mdm.structs}
    s += Emits.emit_struct_switch(mdm, cases, 'o->type', "return 0;")
    s += "} \n"
    return s

Emits.toplevel_methods['packsize'] = emit_toplevel_packsize
Emits.toplevel_headers['packsize'] = "uint32_t lmcp_packsize(lmcp_object* o);\n"

def emit_top_pack_struct(struct):
    header = ""
    header += "if (o==NULL) { \n"
    header += "outb += lmcp_pack_uint8_t(outb, 0); return 1; \n"
    header += "} else { \n"
    header += "outb += lmcp_pack_uint8_t(outb, 1);  \n"
    header += "memcpy(outb, \""+struct.seriesname+"\", 8); outb += 8; \n"
    header += "outb += lmcp_pack_uint32_t(outb, " + struct.id+"); \n"
    header += "outb += lmcp_pack_uint16_t(outb, " + struct.version+"); \n"
    header += "}\n"
    return header

def emit_toplevel_pack(mdm):
    s = "uint32_t lmcp_pack(uint8_t* buf, lmcp_object* o) { \n"
    s += "uint8_t* outb = buf; \n"
    cases = {struct.name : emit_top_pack_struct(struct) + "return 15 + lmcp_pack_"+struct.name+"(outb, ("+struct.name+"*)o);\n" for struct in mdm.structs}
    s += Emits.emit_struct_switch(mdm, cases, 'o->type', "return 0;")
    s += "} \n"
    return s

Emits.toplevel_methods['pack'] = emit_toplevel_pack
Emits.toplevel_headers['pack'] = "uint32_t lmcp_pack(uint8_t* buf, lmcp_object* o);\n"

def emit_toplevel_free(mdm):
    s = "void lmcp_free(lmcp_object *o) { \n"
    cases = {struct.name : "lmcp_free_"+struct.name+"(("+struct.name+"*)o);\n" for struct in mdm.structs}
    s += Emits.emit_struct_switch(mdm, cases, 'o->type', "return;")
    s += "} \n"
    return s
        
Emits.toplevel_methods['free'] = emit_toplevel_free
Emits.toplevel_headers['free'] = "void lmcp_free(lmcp_object* o);\n"

def emit_toplevel_unpack(mdm):
    s = "size_t lmcp_unpack(uint8_t* buf, lmcp_object **o) {\n"
    s += "uint8_t* inb = buf; \n"
    s += "uint32_t tmp; uint16_t tmp16; \n"
    s += "uint8_t isnull; \n"
    s += "uint32_t objtype; uint16_t objseries; char seriesname[8];\n"
    s +=  "inb += lmcp_unpack_uint8_t(inb, &isnull); \n"
    s += "if (isnull == 0) { \n"
    s += "return 1; \n"
    s += "} else { \n"
    s += "memcpy(seriesname, inb, 8); inb += 8; \n"
    s += "inb += lmcp_unpack_uint32_t(inb, &objtype);  \n"
    s += "inb += lmcp_unpack_uint16_t(inb, &objseries);  \n"
    cases = {struct.name : "lmcp_init_"+struct.name+"(("+struct.name+"**)o); \n return 15 + lmcp_unpack_"+struct.name+"(inb, ("+struct.name+"*)(*o));\n" for struct in mdm.structs}
    s += Emits.emit_struct_switch(mdm, cases, 'objtype', "return 15;")
    s += "}\n"
    s += "} \n"
    return s

Emits.toplevel_methods['unpack'] = emit_toplevel_unpack
Emits.toplevel_headers['unpack'] = "size_t lmcp_unpack(uint8_t* buf, lmcp_object **o);\n"





def emit_init(struct):
    header = "void lmcp_init_"+struct.name+" ("+struct.name+"** i) { \n"
    header += "(*i) = malloc(sizeof("+struct.name+"*));\n"
    header += "*(*i) = (const "+struct.name+"){0};\n" 
    #if struct.parent != 'lmcp_object': if needed for something
    #    header += "out += lmcp_init_"+struct.parent+" (&i->super); \n"
    header += "((lmcp_object*)(*i)) -> type = "+struct.id+";\n"
    header += "}\n"
    return header

def emit_init_header(struct):
    return "void lmcp_init_"+struct.name+" ("+struct.name+"** i);\n"

Emits.struct_methods['init'] = emit_init
Emits.struct_headers['init'] = emit_init_header

def emit_sizecalc(struct):
    header = "size_t lmcp_packsize_"+struct.name+" ("+struct.name+"* i) { \n"
    header += "size_t out = 0;\n"
    if struct.parent != 'lmcp_object':
        header += "out += lmcp_packsize_"+struct.parent+"(&(i->super));\n"
    for field in struct.fields:
        if not field.typeinfo.isarray:
            if field.kind == 'base':
                header += "out += sizeof("+TypeInfo.basetypes[field.typeinfo.typename]+");\n"
            elif field.kind == 'enum':
                header += "out += 4;\n"
            elif field.kind == 'struct':
                header += "if (i->"+field.name+"==NULL) { \n"
                header += "out += 1;\n"
                header += "} else {\n"
                header += "out += 15 + lmcp_packsize_"+field.typeinfo.typename+"(i->"+field.name+");}\n"
        else:
            if field.typeinfo.arraysize != "-1": #fixed size
                header += "out += " + field.typeinfo.arraysize + "* sizeof("+TypeInfo.basetypes[field.typeinfo.typename]+");\n"
            else:
                if field.typeinfo.islargearray:
                    header += "out += 4;\n"
                else:
                    header += "out += 2;\n"
                header += "for (uint32_t index = 0; index < i->"+field.name+"_ai.length; index++) { \n"
                if field.kind == 'base':
                    header += "out += sizeof("+TypeInfo.basetypes[field.typeinfo.typename]+");\n"
                elif field.kind == 'enum':
                    header += "out += 4;\n"
                elif field.kind == 'struct': 
                    header += "out += 15 + lmcp_packsize_"+field.typeinfo.typename+"(i->"+field.name+"[index]);\n"
                header += "} \n"
    return header + "return out;} \n"

def emit_sizecalc_header(struct):
    return "size_t lmcp_packsize_"+struct.name+" ("+struct.name+"* i);\n"

Emits.struct_methods['packsize'] = emit_sizecalc
Emits.struct_headers['packsize'] = emit_sizecalc_header


def emit_pack_substruct(field, fieldname, typename):
    header = ""
    header += "if (i->"+fieldname+"==NULL) { \n"
    header += "outb += lmcp_pack_uint8_t(outb, 0);\n"
    header += "} else { \n"
    header += "outb += lmcp_pack_uint8_t(outb, 1);  \n"
    header += "memcpy(outb, \""+field.seriesname+"\", 8); outb += 8; \n"
    header += "outb += lmcp_pack_uint32_t(outb, " + field.id+"); \n"
    header += "outb += lmcp_pack_uint16_t(outb, " + field.version+"); \n"
    header += "outb += lmcp_pack_"+typename+"(outb, i->"+fieldname+"); \n"
    header += "}\n"
    return header


def emit_structpack(struct): 
    header = "size_t lmcp_pack_"+struct.name+"(uint8_t* buf, "+struct.name+"* i) { \n"
    header += "if (i == NULL) return; \n"
    header += "uint8_t* outb = buf;\n"
    if struct.parent != 'lmcp_object':
        header += "outb += lmcp_pack_" + struct.parent +"(outb, &(i->super));\n"
    for field in struct.fields:
        if not field.typeinfo.isarray:
            if field.kind == 'base':
                header += "outb += lmcp_pack_"+TypeInfo.basetypes[field.typeinfo.typename]+"(outb, i->"+field.name+");\n"
            elif field.kind == 'enum':
                header += "outb += lmcp_pack_int32_t(outb, (int) i->"+field.name+");\n"
            elif field.kind == 'struct':
                header += emit_pack_substruct(field, field.name, field.typeinfo.typename)
        else:
            if field.typeinfo.islargearray:
                header += "outb += lmcp_pack_uint32_t(outb, i->"+field.name+"_ai.length);  \n"
            else:
                header += "outb += lmcp_pack_uint16_t(outb, i->"+field.name+"_ai.length);  \n"
            header += "for (uint32_t index = 0; index < i->"+field.name+"_ai.length; index++) {\n"
            if field.kind == 'base':
                header += "outb += lmcp_pack_"+TypeInfo.basetypes[field.typeinfo.typename]+"(outb, i->"+field.name+"[index]); \n"
            elif field.kind == 'enum':
                header += "outb += lmcp_pack_int32_t(outb, (int) i->"+field.name+"[index]);\n"
            elif field.kind == 'struct':
                header += emit_pack_substruct(field, field.name + "[index]", field.typeinfo.typename)
            header += "}\n"
    return header + "return (outb - buf); }\n"

def emit_structpack_header(struct):
    return "size_t lmcp_pack_"+struct.name+"(uint8_t* buf, "+struct.name+"* i);\n"

Emits.struct_methods['pack'] = emit_structpack
Emits.struct_headers['pack'] = emit_structpack_header

def emit_unpack_substruct(struct, fieldname, typename):
    header =  "inb += lmcp_unpack_uint8_t(inb, &isnull); \n"
    header += "if (isnull == 0) { \n"
    header += "out->"+fieldname+" = NULL; \n"
    header += "} else { \n"
    header += "memcpy(seriesname, inb, 8); inb += 8; \n"
    header += "inb += lmcp_unpack_uint32_t(inb, &objtype);  \n"
    header += "inb += lmcp_unpack_uint16_t(inb, &objseries);  \n"
    header += "inb += lmcp_unpack_"+typename+"(inb, &(out->"+fieldname+")); \n"
    header += "}\n"
    return header


def emit_structunpack(struct):
    header = "size_t lmcp_unpack_"+struct.name+"(uint8_t* buf, " + struct.name + "* outp) { \n"
    header += struct.name+"* out = outp;\n"
    header += "uint8_t* inb = buf; \n"
    header += "uint32_t tmp; uint16_t tmp16; \n"
    header += "uint8_t isnull; \n"
    header += "uint32_t objtype; uint16_t objseries; char seriesname[8];\n"
    if struct.parent != 'lmcp_object':
        header += "inb += lmcp_unpack_"+struct.parent+"(inb, &(out->super));\n"
    for field in struct.fields:
        if not field.typeinfo.isarray:
            if field.kind == 'base':
                header += "inb += lmcp_unpack_"+TypeInfo.basetypes[field.typeinfo.typename]+"(inb, &(out->" + field.name+"));\n"
            elif field.kind == 'enum':
                header += "inb += lmcp_unpack_int32_t(inb, (int*) &(out->"+field.name+"));\n"
            elif field.kind == 'struct':
                header += emit_unpack_substruct(struct, field.name, field.typeinfo.typename)
        else:
            if field.typeinfo.islargearray:
                header += "inb += lmcp_unpack_uint32_t(inb, &tmp);\n"
            else:
                header += "inb += lmcp_unpack_uint16_t(inb, &tmp16); tmp = tmp16;\n"
            if field.kind == 'base':
                header += "(out)->"+field.name+" = malloc(sizeof("+TypeInfo.basetypes[field.typeinfo.typename]+"*) * tmp);\n"
            elif field.kind == 'enum':
                header += "(out)->"+field.name+" = malloc(sizeof(int32_t*) * tmp);\n"
            elif field.kind == 'struct':
                header += "(out)->"+field.name+" = malloc(sizeof("+field.typeinfo.typename+"*) * tmp);\n"
            header += "out->"+field.name+"_ai.length = tmp;\n"
            header += "for (uint32_t index = 0; index < out->"+field.name+"_ai.length; index++) {\n"
            if field.kind == 'base':
                header += "inb += lmcp_unpack_"+TypeInfo.basetypes[field.typeinfo.typename]+"(inb, &out->" + field.name+"[index]);\n"
            elif field.kind == 'enum':
                header += "inb += lmcp_unpack_int32_t(inb, (int*) &out->"+field.name+"[index]);\n"
            elif field.kind == 'struct':
                header += emit_unpack_substruct(struct, field.name + "[index]", field.typeinfo.typename)
            header += "}\n"
    return header + "return (inb - buf); }\n"

def emit_structunpack_header(struct):
    return "size_t lmcp_unpack_"+struct.name+"(uint8_t* buf, " + struct.name + "* outp);\n"

Emits.struct_methods['unpack'] = emit_structunpack
Emits.struct_headers['unpack'] = emit_structunpack_header

def emit_free_substruct(struct, fieldname, typename):
    header = "if (out->"+fieldname+" != NULL) {\n"
    header += "lmcp_free_"+typename+"(out->"+fieldname+");\n"
    header += "} \n"
    return header
    

def emit_free(struct):
    header = "void lmcp_free_"+struct.name+"("+struct.name+"* out) {\n"
    header += "if (out == NULL) \n return; \n"
    for field in struct.fields:
        if not field.typeinfo.isarray:
            if field.kind == 'struct':
                header += emit_free_substruct(struct, field.name, field.typeinfo.typename)
        else:
            header += "if (out->"+field.name+" != NULL) { \n"
            if field.kind == 'base' or field.kind == 'enum':
                header += "free (out->"+field.name+"); \n"
            else:
                header += "for (uint32_t index = 0; index < out->"+field.name+"_ai.length; index++) {\n"
                header += emit_free_substruct(struct, field.name+"[index]", field.typeinfo.typename)
                header += "}\n"
            header += "free(out->"+field.name+");\n"
            header += "} \n"
    header += "free(out);\n"
    header += "} \n"            
    return header

def emit_free_header(struct):
    return "void lmcp_free_"+struct.name+"("+struct.name+"* i); \n"

Emits.struct_methods['free'] = emit_free
Emits.struct_headers['free'] = emit_free_header
