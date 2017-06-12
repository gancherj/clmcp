
#pragma once
#include <stdlib.h>
#include <inttypes.h>
#include <string.h>
#include "common/struct_defines.h"
#include "common/conv.h"
#define LMCP_TestStruct_SUB "mytst.tst.TestStruct"

#define LMCP_TestStruct_TYPENAME "TestStruct"

typedef struct {
    lmcp_object super;
    uint32_t tstfield;

} TestStruct;
size_t lmcp_packsize_TestStruct (TestStruct* i);
size_t lmcp_pack_TestStruct_header(uint8_t* buf, TestStruct* i);
void lmcp_free_TestStruct(TestStruct* i);
void lmcp_init_TestStruct (TestStruct** i);
void lmcp_unpack_TestStruct(uint8_t** buf, size_t *size_remain,TestStruct* outp);
size_t lmcp_pack_TestStruct(uint8_t* buf, TestStruct* i);
