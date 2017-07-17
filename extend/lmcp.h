#pragma once
#include "common/struct_defines.h"
#include "Struct1.h"
#include "Struct2.h"
uint32_t lmcp_msgsize(lmcp_object* o);
uint32_t lmcp_packsize(lmcp_object* o);
void lmcp_free(lmcp_object* o);
void lmcp_make_msg(uint8_t* buf, lmcp_object *o);
void lmcp_process_msg(uint8_t** inb, size_t size, lmcp_object **o);
void lmcp_unpack(uint8_t** inb, size_t size, lmcp_object **o);
uint32_t lmcp_pack(uint8_t* buf, lmcp_object* o);
