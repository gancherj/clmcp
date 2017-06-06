#include <stdio.h>
#include "Struct2.h"
#include "Struct1.h"

int main() {
    Struct2 s2;
    lmcp_init_Struct2(&s2);
    s2.field2 = malloc(5 * sizeof(Struct1*));
    s2.field2_ai.length = 5;
    for (int i = 0; i < 5; i++) {
        s2.field2[i] = malloc(sizeof(Struct1));
        lmcp_init_Struct1(s2.field2[i]);
        s2.field2[i]->field1 = i;
    }

    uint8_t* buf = malloc(lmcp_packsize_Struct2(&s2));
    lmcp_pack_Struct2(buf, &s2);
    Struct2 *s;
    lmcp_unpack_Struct2(buf, &s);

    for (int i =0; i < 5; i++ )
        printf("%d\n", s->field2[i]->field1);
}
