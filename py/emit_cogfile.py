import MDM

import xml.etree.ElementTree as ET

def emit_struct(struct, filename, outdir, templ, mdm):
    return (templ + " -D version=" + mdm.version + " -D namespace="+mdm.namespace+" -D series="+mdm.seriesname+" -D mdm="+filename+" -D struct="+struct.attrib['Name']+" -o "+outdir+struct.attrib['Name']+".c")

def emit_enum(enum, filename, outdir, templ, mdm):
    return (templ + " -D version=" + mdm.version + " -D namespace="+mdm.namespace+" -D series="+mdm.seriesname+" -D mdm="+filename+" -D enum="+enum.attrib['Name']+" -o "+outdir+enum.attrib['Name']+".c")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("usage: " + sys.argv[0] + " in.mdm outdir struct_templ.c enum_templ.c")
        sys.exit()
    else:
        mdm = read_mdm(sys.argv[1])
        for enum in mdm.enums:
            print(emit_enum(enum, sys.argv[1], sys.argv[2], sys.argv[4], mdm))
        for struct in mdm.structs:
            print(emit_struct(struct, sys.argv[1], sys.argv[2], sys.argv[3], mdm))
