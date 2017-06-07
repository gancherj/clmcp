#pragma once
#include "common/struct_defines.h"
#include "Struct1.h"
#include "Struct2.h"
uint32_t lmcp_packsize(lmcp_object* o);
size_t lmcp_unpack(uint8_t* buf, lmcp_object **o);
void lmcp_free(lmcp_object* o);
uint32_t lmcp_pack(uint8_t* buf, lmcp_object* o);
