
#include <stdlib.h>
#include <inttypes.h>
#include "Struct2.h"
uint32_t lmcp_packsize_Struct2 (Struct2* i) { 
uint32_t out = 0;
out += lmcp_packsize_Struct1(i->super);
out += sizeof(uint32_t);
return out;} 
size_t lmcp_unpack_Struct2(uint8_t* buf, Struct2** outp) { 
*outp = malloc(sizeof(Struct2));
Struct2* out = *outp;
uint8_t* inb = buf; 
uint32_t tmp; uint16_t tmp16; 
uint8_t isnull; 
uint32_t objtype; uint32_t objseries; 
inb += lmcp_unpack_Struct1(inb, &(out->super));
inb += lmcp_unpack_uint32_t(inb, &(out->field2));
return (inb - buf); }
void lmcp_init_Struct2 (Struct2* i) { 
(*i) = (const Struct2){0};
((lmcp_object*)i) -> type = 2;
}
size_t lmcp_pack_Struct2(uint8_t* buf, Struct2* i) { 
uint8_t* outb = buf;
outb += lmcp_pack_Struct1(outb, i->super);
outb += lmcp_pack_uint32_t(outb, i->field2);
return (outb - buf); }