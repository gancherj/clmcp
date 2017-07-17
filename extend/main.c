#include <stdio.h>
#include "lmcp.h"

int main() {
    Struct2* s2;
    lmcp_init_Struct2(&s2);
    s2->super.field1 = 1234;
    s2->field2 = 5678;

    size_t packsize = lmcp_packsize((lmcp_object*)s2);
    uint8_t* buf = malloc(packsize);
    lmcp_pack(buf, (lmcp_object*)s2);

    Struct2 *s;
    uint8_t* inb = buf;
    lmcp_unpack(&inb, packsize, (lmcp_object**)&s);
    printf("%d\n", ((lmcp_object*)s)->type);
    printf("%d\n", s->super.field1);
    printf("%d\n", s->field2);

    lmcp_free((lmcp_object*)s2);
    lmcp_free((lmcp_object*)s);
    free(buf);

}
