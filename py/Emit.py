from MDM import *

# emit_sizecalc: structinfo -> string
# emit_structpack: structinfo -> string
# emit_structunpack: structinfo -> string


class Emits:
    methods = {}
    headers = {}
    @staticmethod
    def header_filename(struct):
        return struct.name+".h"
    @staticmethod
    def c_filename(struct):
        return struct.name+".c"
    @staticmethod
    def emit_header_top():
        return '''
#pragma once
#include <stdlib.h>
#include <inttypes.h>
#include <string.h>
#include "common/struct_defines.h"
#include "common/conv.h"
'''

    @staticmethod
    def emit_header(struct):
        s = ""
        if struct.parent != 'lmcp_object':
            s += '#include \"'+struct.parent+'\"\n'
        for h in Emits.headers:
            s += (Emits.headers[h])(struct)
        return s
    @staticmethod
    def emit_c(struct):
        s = ""
        s += '''
#include <stdlib.h>
#include <inttypes.h>
'''
        s += '#include \"'+struct.name+'.h\"\n'
        for m in Emits.methods:
            s += (Emits.methods[m])(struct)
        return s

def emit_init(struct):
    header = "void lmcp_init_"+struct.name+" ("+struct.name+"* i) { \n"
    header += "(*i) = (const "+struct.name+"){0};\n" 
    #if struct.parent != 'lmcp_object': if needed for something
    #    header += "out += lmcp_init_"+struct.parent+" (&i->super); \n"
    header += "((lmcp_object*)i) -> type = "+struct.id+";\n"
    header += "}\n"
    return header

def emit_init_header(struct):
    return "void lmcp_init_"+struct.name+" ("+struct.name+"* i);\n"

Emits.methods['init'] = emit_init
Emits.headers['init'] = emit_init_header

def emit_sizecalc(struct):
    header = "uint32_t lmcp_packsize_"+struct.name+" ("+struct.name+"* i) { \n"
    header += "uint32_t out = 0;\n"
    if struct.parent != 'lmcp_object':
        header += "out += lmcp_packsize_"+struct.parent+"(i->super);\n"
    for field in struct.fields:
        if not field.typeinfo.isarray:
            if field.typeinfo.typename in TypeInfo.basetypes:
                header += "out += sizeof("+TypeInfo.basetypes[field.typeinfo.typename]+");\n"
            else:
                header += "if (i->"+field.name+"==NULL) { \n"
                header += "out += 1\n"
                header += "else {\n"
                header += "out += 15 + lmcp_"+field.typeinfo.typename+"_packsize(i->"+field.name+");}\n"
        else:
            if field.typeinfo.arraysize != "-1": #fixed size
                header += "out += " + field.typeinfo.arraysize + "* sizeof("+TypeInfo.basetypes[field.typeinfo.typename]+");\n"
            else:
                if field.typeinfo.islargearray:
                    header += "out += 4;\n"
                else:
                    header += "out += 2;\n"
                header += "for (uint32_t index = 0; index < i->"+field.name+"_ai.length; index++) { \n"
                if field.typeinfo.typename in TypeInfo.basetypes:
                    header += "out += sizeof("+TypeInfo.basetypes[field.typeinfo.typename]+");\n"
                else: 
                    header += "out += 15 + lmcp_"+field.typeinfo.typename+"_packsize(i->"+field.name+"[index]);\n"
                header += "} \n"
    return header + "return out;} \n"

def emit_sizecalc_header(struct):
    return "uint32_t lmcp_packsize_"+struct.name+" ("+struct.name+"* i);\n"

Emits.methods['sizecalc'] = emit_sizecalc
Emits.headers['sizecalc'] = emit_sizecalc_header


def emit_pack_substruct(struct, fieldname, typename):
    header = ""
    header += "if (i->"+fieldname+"==NULL) { \n"
    header += "lmcp_pack_uint8_t(outb, 0); outb += 1;\n"
    header += "} else { \n"
    header += "lmcp_pack_uint8_t(outb, 1); outb += 1; \n"
    header += "memcpy(outb, \""+struct.seriesname+"\", 8); outb += 8; \n"
    header += "lmcp_pack_uint32_t(outb, " + struct.id+"); outb += 4; \n"
    header += "lmcp_pack_uint16_t(outb, " + struct.version+"); outb += 2; \n"
    header += "lmcp_pack_"+typename+"(outb, i->"+fieldname+"); outb += lmcp_"+typename+"_packsize(i->"+fieldname+");\n"
    header += "}\n"
    return header


def emit_structpack(struct): 
    header = "void lmcp_pack_"+struct.name+"(uint8_t* buf, "+struct.name+"* i) { \n"
    header += "uint8_t* outb = buf;\n"
    if struct.parent != 'lmcp_object':
        header += "lmcp_pack_" + struct.parent +"(outb, i->super);\n"
    for field in struct.fields:
        if not field.typeinfo.isarray:
            if field.typeinfo.typename in TypeInfo.basetypes:
                header += "lmcp_pack_"+TypeInfo.basetypes[field.typeinfo.typename]+"(outb, i->"+field.name+");\n"
            else:
                header += emit_pack_substruct(struct, field.name, field.typeinfo.typename)
        else:
            if field.typeinfo.islargearray:
                header += "lmcp_pack_uint32_t(outb, i->"+field.name+"_ai.length); outb += 4; \n"
            else:
                header += "lmcp_pack_uint16_t(outb, i->"+field.name+"_ai.length); outb += 2; \n"
            header += "for (uint32_t index = 0; index < i->"+field.name+"_ai.length; index++) {\n"
            if field.typeinfo.typename in TypeInfo.basetypes:
                header += "lmcp_pack_"+TypeInfo.basetypes[field.typeinfo.typename]+"(outb, i->"+field.name+"[index]); outb += sizeof("+TypeInfo.basetypes[field.typeinfo.typename]+");\n"
            else:
                header += emit_pack_substruct(struct, field.name + "[index]", field.typeinfo.typename)
            header += "}\n"
    return header + "}\n"

def emit_structpack_header(struct):
    return "void lmcp_pack_"+struct.name+"(uint8_t* buf, "+struct.name+"* i);\n"

Emits.methods['structpack'] = emit_structpack
Emits.headers['structpack'] = emit_structpack_header

def emit_unpack_substruct(struct, fieldname, typename):
    header =  "inb += lmcp_unpack_uint8_t(inb, &isnull); \n"
    header += "if (isnull == 0) { \n"
    header += "out->"+fieldname+" = NULL; \n"
    header += "} else { \n"
    header += "out->"+fieldname+" = malloc(sizeof("+typename+"));\n"
    header += "inb += lmcp_unpack_uint32_t(inb, &objtype);  \n"
    header += "inb += lmcp_unpack_uint16_t(inb, &objseries);  \n"
    header += "inb += lmcp_unpack_"+typename+"(inb, &(out->"+fieldname+")); \n"
    return header


def emit_structunpack(struct):
    header = "void lmcp_unpack_"+struct.name+"(uint8_t* buf, " + struct.name + "** outp) { \n"
    header += "*outp = malloc(sizeof("+struct.name+"));\n"
    header += struct.name+"* out = *outp;\n"
    header += "uint8_t* inb = buf; \n"
    header += "uint32_t tmp; uint16_t tmp16; \n"
    header += "uint8_t isnull; \n"
    header += "uint32_t objtype; uint32_t objseries; \n"
    if struct.parent != 'lmcp_object':
        header += "inb += lmcp_unpack_"+struct.parent+"(inb, &(i->super));\n"
    for field in struct.fields:
        if not field.typeinfo.isarray:
            if field.typeinfo.typename in TypeInfo.basetypes:
                header += "inb += lmcp_unpack_"+TypeInfo.basetypes[field.typeinfo.typename]+"(inb, &(out->" + field.name+"));\n"
            else:
                header += emit_unpack_substruct(struct, field.name, field.typeinfo.typename)
        else:
            if field.typeinfo.islargearray:
                header += "inb += lmcp_unpack_uint32_t(inb, &tmp);\n"
            else:
                header += "inb += lmcp_unpack_uint16_t(inb, &tmp16); tmp = tmp16;\n"
            if field.typeinfo.typename in TypeInfo.basetypes:
                header += "(out)->"+field.name+" = malloc(sizeof("+TypeInfo.basetypes[field.typeinfo.typename]+") * tmp);\n"
            else:
                header += "(out)->"+field.name+" = malloc(sizeof("+field.typeinfo.typename+") * tmp);\n"
            header += "out->"+field.name+"_ai.length = tmp;\n"
            header += "for (uint32_t index = 0; index < out->"+field.name+"_ai.length; index++) {\n"
            if field.typeinfo.typename in TypeInfo.basetypes:
                header += "inb += lmcp_unpack_"+TypeInfo.basetypes[field.typeinfo.typename]+"(inb, &out->" + field.name+"[index]);\n"
            else:
                header += emit_unpack_substruct(struct, field.name + "[index]", field.typeinfo.typename)
            header += "}\n"
    return header + "}\n"

def emit_structunpack_header(struct):
    return "void lmcp_unpack_"+struct.name+"(uint8_t* buf, " + struct.name + "** outp);\n"

Emits.methods['structunpack'] = emit_structunpack
Emits.headers['structunpack'] = emit_structunpack_header
