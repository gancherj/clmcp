struct_templ = '''
#define LMCP_{struct_name}_SUB "{struct_subscription}"
#define LMCP_{struct_name}_TYPENAME "{struct_name}"
typedef struct {{
    {struct_parent} super;
    {struct_fields}
}} {struct_name}; 
'''

sizecalc_tmpl = '''
uint32_t lmcp_{struct_name}_packsize ({struct_name}* s) {
    uint32_t out = 0;
    out += lmcp_{struct_parent}_packsize(s->super);
    {field_sizecalcs}
    return out;
}'''

field_sizecalc_tmpl_prim = "out += sizeof({prim_type});"
field_sizecalc_tmpl_struct = '''
if (i->{field_name} == NULL) {
    out += 1;
}
else {
    out += 15 + lmcp_{field_typename}_packsize(i->{field_name});
    }'''
field_sizecalc_tmpl_array

