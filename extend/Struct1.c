
#include <stdlib.h>
#include <inttypes.h>
#include "Struct1.h"
uint32_t lmcp_packsize_Struct1 (Struct1* i) { 
uint32_t out = 0;
out += sizeof(uint32_t);
return out;} 
size_t lmcp_unpack_Struct1(uint8_t* buf, Struct1** outp) { 
*outp = malloc(sizeof(Struct1));
Struct1* out = *outp;
uint8_t* inb = buf; 
uint32_t tmp; uint16_t tmp16; 
uint8_t isnull; 
uint32_t objtype; uint32_t objseries; 
inb += lmcp_unpack_uint32_t(inb, &(out->field1));
return (inb - buf); }
void lmcp_init_Struct1 (Struct1* i) { 
(*i) = (const Struct1){0};
((lmcp_object*)i) -> type = 1;
}
size_t lmcp_pack_Struct1(uint8_t* buf, Struct1* i) { 
uint8_t* outb = buf;
outb += lmcp_pack_uint32_t(outb, i->field1);
return (outb - buf); }
