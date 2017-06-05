import MDM, sys, Emit

def emit_methods(mdm):
    for struct in mdm.structs:
        print(Emit.emit_sizecalc(struct))
        print(Emit.emit_structpack(struct))
        print(Emit.emit_structunpack(struct))

if __name__ == "__main__":
    mdm = MDM.MDM(sys.argv[1])
    print('''
#include <stdlib.h>
#include <string.h>
#include "struct_defines.h"
#include "conv.h"''')
    print(mdm.emit())
    emit_methods(mdm)
    
