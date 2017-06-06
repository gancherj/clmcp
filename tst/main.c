#include "Struct2.h"

int main() {
    Struct2* s;
    lmcp_init_Struct2 (&s);

    s->field2 = malloc(5 * sizeof(Struct1*));

    lmcp_free_Struct2(s);
}

