#include "Struct2.h"
#include <stdio.h>

int main(int argc, char** argv) {


    FILE* f = fopen(argv[1], "rb");
    fseek(f, 0, SEEK_END);
    size_t fsize = ftell(f);
    fseek(f, 0, SEEK_SET);
    uint8_t* buf = malloc(fsize);
    fread(buf, 1, fsize, f);
    fclose(f);


    Struct2 *s;
    lmcp_unpack_Struct2(buf, &s);

    printf("%d\n", s->field2->field1);

    lmcp_free_Struct2(s);

}
