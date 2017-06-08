#include <stdio.h>
#include "lmcp.h"

int main() {
    Struct2 *s2;
    lmcp_init_Struct2(&s2);
    s2->field2 = malloc(5 * sizeof(Struct1*));
    s2->field2_ai.length = 5;
    for (int i = 0; i < 5; i++) {
        lmcp_init_Struct1(&s2->field2[i]);
        s2->field2[i]->field1 = i;
    }

    uint8_t* buf = malloc(lmcp_packsize((lmcp_object*)s2));
    lmcp_pack(buf, (lmcp_object*)s2);

    Struct2 *s;
    lmcp_unpack(buf, (lmcp_object**)&s);

    for (int i =0; i < 5; i++ )
        printf("%d\n", s->field2[i]->field1);

    free(buf);
    lmcp_free((lmcp_object*)s);
    lmcp_free((lmcp_object*)s2);
}
