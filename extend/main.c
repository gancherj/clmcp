#include <stdio.h>
#include "lmcp.h"

int main() {
    Struct2* s2;
    lmcp_init_Struct2(&s2);
    printf("%d\n", ((lmcp_object*)s2)->type);
    s2->super.field1 = 1234;
    s2->field2 = 5678;

    uint8_t* buf = malloc(lmcp_packsize((lmcp_object*)s2));
    printf("%d\n", lmcp_packsize((lmcp_object*)s2));
    lmcp_pack(buf, (lmcp_object*)s2);

    Struct2 *s;

    lmcp_unpack(buf, (lmcp_object**)&s);
    printf("%d\n", ((lmcp_object*)s)->type);
    printf("%d\n", s->super.field1);


    lmcp_free((lmcp_object*)s2);
    lmcp_free((lmcp_object*)s);
    free(buf);

}
