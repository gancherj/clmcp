from MDM import *

# emit_sizecalc: structinfo -> string
# emit_structpack: structinfo -> string
# emit_structunpack: structinfo -> string

# inb += unpack(inb, &out) -> inb = unpack(inb, outb, size, &out)
# unpack(uint8_t **inb, size_remain, out): if (size_remain < amount to read) or inb == NULL then return NULL else do the unpack; increment inb



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
        s += '#include \"lmcp.h\"\n'
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
    cases = {struct.name : "return 15 + lmcp_packsize_"+struct.name+"(("+struct.name+"*)o);\n" for struct in mdm.structs}
    s += Emits.emit_struct_switch(mdm, cases, 'o->type', "return 0;")
    s += "} \n"
    return s

Emits.toplevel_methods['packsize'] = emit_toplevel_packsize
Emits.toplevel_headers['packsize'] = "uint32_t lmcp_packsize(lmcp_object* o);\n"


def emit_toplevel_pack(mdm):
    s = "uint32_t lmcp_pack(uint8_t* buf, lmcp_object* o) { \n"
    s += "uint8_t* outb = buf; \n"
    cases = {struct.name : "outb += lmcp_pack_"+struct.name+"_header(outb, ("+struct.name+"*)o); outb += lmcp_pack_"+struct.name+"(outb, ("+struct.name+"*)o); return (outb - buf);\n" for struct in mdm.structs}
    s += Emits.emit_struct_switch(mdm, cases, 'o->type', "return 0;")
    s += "} \n"
    return s

Emits.toplevel_methods['pack'] = emit_toplevel_pack
Emits.toplevel_headers['pack'] = "uint32_t lmcp_pack(uint8_t* buf, lmcp_object* o);\n"

def emit_toplevel_free(mdm):
    s = "void lmcp_free(lmcp_object *o) { \n"
    s += "if (o == NULL) {return; }\n"
    cases = {struct.name : "lmcp_free_"+struct.name+"(("+struct.name+"*)o);\n" for struct in mdm.structs}
    s += Emits.emit_struct_switch(mdm, cases, 'o->type', "return;")
    s += "} \n"
    return s
        
Emits.toplevel_methods['free'] = emit_toplevel_free
Emits.toplevel_headers['free'] = "void lmcp_free(lmcp_object* o);\n"

def emit_toplevel_unpack(mdm):
    s = "void lmcp_unpack(uint8_t** inb, size_t size, lmcp_object **o) {\n"
    s += "if (o == NULL) return;\n"
    s += "size_t* size_remain = &size;\n"
    s += "uint32_t tmp; uint16_t tmp16; \n"
    s += "int isnull; \n"
    s += "uint32_t objtype; uint16_t objseries; char seriesname[8];\n"
    s += "isnull = lmcp_unpack_structheader(inb, size_remain, seriesname, &objtype, &objseries);\n"
    s += "if (isnull == 0) { *o = NULL; return; }"
    cases = {struct.name : "lmcp_init_"+struct.name+"(("+struct.name+"**)o); \n lmcp_unpack_"+struct.name+"(inb, size_remain, ("+struct.name+"*)(*o));\n" for struct in mdm.structs}
    s += Emits.emit_struct_switch(mdm, cases, 'objtype', "return;")
    s += "}\n"
    return s

Emits.toplevel_methods['unpack'] = emit_toplevel_unpack
Emits.toplevel_headers['unpack'] = "void lmcp_unpack(uint8_t** inb, size_t size, lmcp_object **o);\n"


def emit_toplevel_processmsg(mdm):
    s = "void lmcp_process_msg(uint8_t** inb, size_t size, lmcp_object **o) {\n"
    s += "if (size < 8) {return;}\n"
    s += "if (inb == NULL || *inb == NULL) { *o = NULL; return; } \n"
    s += "if ((*inb)[0] != 'L' || (*inb)[1] != 'M' || (*inb)[2] != 'C' || (*inb)[3] != 'P') { return; } \n"
    s += "*inb += 4;\n"
    s += "size_t s = 4;\n"
    s += "uint32_t msglen;\n"
    s += "lmcp_unpack_uint32_t(inb, &s, &msglen);\n"
    s += "if (size < (msglen + 8)) { *o = NULL; *inb = NULL; return;} \n"
    s += "lmcp_unpack(inb, msglen, o);\n"
    s += "}\n"
    return s

Emits.toplevel_methods['processmsg'] = emit_toplevel_processmsg
Emits.toplevel_headers['processmsg'] = "void lmcp_process_msg(uint8_t** inb, size_t size, lmcp_object **o);\n"

def emit_toplevel_msgsize(mdm):
    s = "uint32_t lmcp_msgsize(lmcp_object* o) { return 8 + lmcp_packsize(o); }\n"
    return s

Emits.toplevel_methods['msgsize'] = emit_toplevel_msgsize
Emits.toplevel_headers['msgsize'] = "uint32_t lmcp_msgsize(lmcp_object* o);\n"

def emit_toplevel_makemsg(mdm):
    s = "void lmcp_make_msg(uint8_t* buf, lmcp_object* o) { \n"
    s += "buf[0] = 'L'; buf[1] = 'M'; buf[2] = 'C'; buf[3] = 'P'; \n"
    s += "lmcp_pack_uint32_t(buf+4, lmcp_packsize(o));\n"
    s += "lmcp_pack(buf + 8, o);\n"
    s += "}\n"
    return s

Emits.toplevel_methods['makemsg'] = emit_toplevel_makemsg
Emits.toplevel_headers['makemsg'] = "void lmcp_make_msg(uint8_t* buf, lmcp_object *o);\n"

def emit_init(struct):
    header = "void lmcp_init_"+struct.name+" ("+struct.name+"** i) { \n"
    header += "if (i == NULL) return;\n"
    header += "(*i) = malloc(sizeof("+struct.name+"));\n"
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

def emit_pack_struct_header(struct):
    s = "size_t lmcp_pack_"+struct.name+"_header(uint8_t* buf, "+struct.name+"* i) { \n"
    s += "uint8_t* outb = buf;\n"
    s += "if (i == NULL) { lmcp_pack_uint8_t(outb, 0); return 1;}"
    s += "outb += lmcp_pack_uint8_t(outb, 1); \n"
    s += "memcpy(outb, \""+struct.seriesname+"\", "+len(struct.seriesname)+"); outb += "len(struct.seriesname)"; \n"
    s += "for (size_t j = "len(struct.seriesname)"; j < 8; j++)\n"
    s += "outb[j] = 0;"
    s += "outb += lmcp_pack_uint32_t(outb, " + struct.id+"); \n"
    s += "outb += lmcp_pack_uint16_t(outb, " + struct.version+"); \n"
    s += "return 15;\n"
    s += "}\n"
    return s

def emit_pack_struct_header_header(struct):
    return "size_t lmcp_pack_"+struct.name+"_header(uint8_t* buf, "+struct.name+"* i);\n"

Emits.struct_methods['packstructheader'] = emit_pack_struct_header
Emits.struct_headers['packstructheader'] = emit_pack_struct_header_header

def emit_pack_substruct(field, fieldname, typename):
    header = ""
    header += "if (i->"+fieldname+"==NULL) { \n"
    header += "outb += lmcp_pack_uint8_t(outb, 0);\n"
    header += "} else { \n"
    header += "outb += lmcp_pack_uint8_t(outb, 1);  \n"
    header += "memcpy(outb, \""+struct.seriesname+"\", "+len(struct.seriesname)+"); outb += "len(struct.seriesname)"; \n"
    header += "for (size_t j = "len(struct.seriesname)"; j < 8; j++)\n"
    header += "outb[j] = 0;"
    header += "outb += lmcp_pack_uint32_t(outb, " + field.id+"); \n"
    header += "outb += lmcp_pack_uint16_t(outb, " + field.version+"); \n"
    header += "outb += lmcp_pack_"+typename+"(outb, i->"+fieldname+"); \n"
    header += "}\n"
    return header



def emit_structpack(struct): 
    header = "size_t lmcp_pack_"+struct.name+"(uint8_t* buf, "+struct.name+"* i) { \n"
    header += "if (i == NULL) return 0; \n"
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
    header =  "lmcp_unpack_uint8_t(inb, size_remain, &isnull); \n"
    header += "if (isnull == 0 && inb != NULL) { \n"
    header += "out->"+fieldname+" = NULL; \n"
    header += "} else if (inb != NULL) { \n"
    header += "lmcp_unpack_8byte(inb, size_remain, seriesname); \n"
    header += "lmcp_unpack_uint32_t(inb, size_remain, &objtype);  \n"
    header += "lmcp_unpack_uint16_t(inb, size_remain, &objseries);  \n"
    header += "lmcp_init_"+typename+"(&(out->"+fieldname+"));\n"
    header += "lmcp_unpack_"+typename+"(inb, size_remain, (out->"+fieldname+")); \n"
    header += "}\n"
    return header


def emit_structunpack(struct):
    h = "void lmcp_unpack_"+struct.name+"(uint8_t** inb, size_t *size_remain, " + struct.name + "* outp) { \n"
    h += "if (inb == NULL || *inb == NULL) { *inb = NULL; return; }\n"
    h += "if (size_remain == NULL || *size_remain == 0) {*inb = NULL; return;} \n" 
    h += struct.name+"* out = outp;\n"
    h += "uint32_t tmp; uint16_t tmp16; \n"
    h += "uint8_t isnull; \n"
    h += "uint32_t objtype; uint16_t objseries; char seriesname[8];\n"
    if struct.parent != 'lmcp_object':
        h += "lmcp_unpack_"+struct.parent+"(inb, size_remain, &(out->super));\n"
    for field in struct.fields:
        if not field.typeinfo.isarray:
            if field.kind == 'base':
                h += "lmcp_unpack_"+TypeInfo.basetypes[field.typeinfo.typename]+"(inb, size_remain, &(out->" + field.name+"));\n"
            elif field.kind == 'enum':
                h += "lmcp_unpack_int32_t(inb, size_remain, (int*) &(out->"+field.name+"));\n"
            elif field.kind == 'struct':
                h += emit_unpack_substruct(struct, field.name, field.typeinfo.typename)
        else:
            if field.typeinfo.islargearray:
                h += "lmcp_unpack_uint32_t(inb, size_remain, &tmp);\n"
            else:
                h += "lmcp_unpack_uint16_t(inb, size_remain, &tmp16); tmp = tmp16;\n"
            if field.kind == 'base':
                h += "(out)->"+field.name+" = malloc(sizeof("+TypeInfo.basetypes[field.typeinfo.typename]+") * tmp);\n"
            elif field.kind == 'enum':
                h += "(out)->"+field.name+" = malloc(sizeof(int32_t) * tmp);\n"
            elif field.kind == 'struct':
                h += "(out)->"+field.name+" = malloc(sizeof("+field.typeinfo.typename+") * tmp);\n"
            h += "if (out->"+field.name+"==0) { *inb = NULL; return; }\n"
            h += "out->"+field.name+"_ai.length = tmp;\n"
            h += "for (uint32_t index = 0; index < out->"+field.name+"_ai.length; index++) {\n"
            if field.kind == 'base':
                h += "lmcp_unpack_"+TypeInfo.basetypes[field.typeinfo.typename]+"(inb, size_remain, &out->" + field.name+"[index]);\n"
            elif field.kind == 'enum':
                h += "lmcp_unpack_int32_t(inb, size_remain, (int*) &out->"+field.name+"[index]);\n"
            elif field.kind == 'struct':
                h += emit_unpack_substruct(struct, field.name + "[index]", field.typeinfo.typename)
            h += "}\n"
    return h + " }\n"

def emit_structunpack_header(struct):
    return "void lmcp_unpack_"+struct.name+"(uint8_t** buf, size_t *size_remain," + struct.name + "* outp);\n"

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
                pass
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
