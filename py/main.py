import MDM, os, errno
import subprocess
from Emit import Emits
import argparse
import shutil
import sys 

def ensure_path(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def emit(path, filename):
    ensure_path(path)
    ensure_path(os.path.join(path, 'common'))
    mdm = MDM.MDM(filename)

    for struct in mdm.structs:
        f = open(os.path.join(path, Emits.header_filename(struct)), 'w')
        f.write(Emits.emit_header_top(struct))
        f.write(struct.emit())
        f.write(Emits.emit_struct_header(struct))
        f.close()

        f = open(os.path.join(path, Emits.c_filename(struct)), 'w')
        f.write(Emits.emit_c(struct))
        f.close()
        
    if len(mdm.enums) > 0:
        f = open(os.path.join(path, 'enums.h'), 'w')
        f.write("#pragma once\n")
        for enum in mdm.enums:
            f.write(enum.emit())
        f.close()
   
    f = open(os.path.join(path, 'lmcp.h'), 'w')
    f.write(Emits.emit_toplevel_header(mdm))
    f.close()

    f = open(os.path.join(path, 'lmcp.c'), 'w')
    f.write(Emits.emit_toplevel_c(mdm))
    f.close()


    csrc_folder = os.path.join(get_script_path(), 'csrc')
    common_files = os.listdir(csrc_folder)
    for c in common_files:
        if os.path.isfile(os.path.join(csrc_folder, c)):
            shutil.copy(os.path.join(csrc_folder, c), os.path.join(path, 'common'))

    subprocess.call(["astyle", "-n", os.path.join(path, "*.c"), os.path.join(path,"*.h")])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates C code from MDM file.")
    parser.add_argument('--dir', nargs=1, help="output directory")
    parser.add_argument('--mdm', nargs=1, help="input mdm")
    args = parser.parse_args()
    output_dir = args.dir[0]
    in_file = args.mdm[0]
    emit(output_dir, in_file)
