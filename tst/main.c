#include "lmcp.h"

uint32_t f(uint32_t i) {
    TestStruct *ts;
    lmcp_init_TestStruct(&ts);

    //ts->tstfield = i;

    //uint8_t* buf  = malloc(lmcp_msgsize((lmcp_object*)ts));
    //lmcp_make_msg(buf, (lmcp_object*)ts);

    //TestStruct *ts2 = NULL;
    //uint8_t* inb = buf;
    //lmcp_process_msg(&inb, lmcp_msgsize((lmcp_object*)ts), (lmcp_object**)&ts2);

    uint32_t out = ts2->tstfield;

    free(buf);
    lmcp_free_TestStruct(ts);
    lmcp_free_TestStruct(ts2);
    return out;
}

void g() {
    TestStruct *ts;
    lmcp_init_TestStruct(&ts);
    //lmcp_free((lmcp_object*)ts);
    if (ts != NULL)
        free(ts);
}

int main() {
    printf("%u", f(37));
}




