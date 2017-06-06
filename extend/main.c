#include <stdio.h>
#include "Struct2.h"

int main() {
    Struct2 s2;
    lmcp_init_Struct2(&s2);
    s2.super = malloc(sizeof(Struct1));
    s2.super->field1 = 42;
    
    uint8_t* buf = malloc(lmcp_packsize_Struct2(&s2));
    lmcp_pack_Struct2(buf, &s2);

    Struct2 *s;

    lmcp_unpack_Struct2(buf, &s);
    printf("%d\n", s->super->field1);

}
