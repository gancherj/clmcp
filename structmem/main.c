#include "Struct2.h"
#include <stdio.h>

int main() {

    Struct2 s2;
    lmcp_init_Struct2(&s2);

    s2.field2 = malloc(sizeof(Struct1));
    s2.field2->field1 = 66;

    uint8_t* buf = malloc(lmcp_packsize_Struct2(&s2));
    printf("packsize: %d\n", lmcp_packsize_Struct2(&s2));
    lmcp_pack_Struct2(buf, &s2);

    Struct2 *s;
    lmcp_unpack_Struct2(buf, &s);

    printf("%d\n", s->field2->field1);
}
