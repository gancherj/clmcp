#include "lmcp.h"
#include <stdio.h>

int main(int argc, char** argv) {

    Struct2 *s;
    lmcp_init_Struct2(&s);
    s->field2 = malloc(sizeof(Struct1));
    s->field2->field1 = 42;

    uint8_t* buf = malloc(lmcp_packsize((lmcp_object*)s));
    lmcp_pack(buf, (lmcp_object*) s);

    Struct2 *s2;
    lmcp_unpack(buf, (lmcp_object**)&s2);

    printf("%d\n", s2->field2->field1);

    lmcp_free((lmcp_object*)s);
    lmcp_free((lmcp_object*)s2);
    free(buf);
}
