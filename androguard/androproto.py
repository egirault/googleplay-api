#!/usr/bin/python
# This script analyzes an APK and tries to recover its .proto file, assuming
# the APK is using Micro-Protobuf. It has only been tested on Google Play
# Android client (sha1: 0f214c312f9800b01e2a5a7b9766dc880efda110).
#
# Use it at your own risk!

import sys

from pprint import pprint

from androguard.core import *
from androguard.core.androgen import *
from androguard.core.androconf import *
from androguard.core.bytecode import *
from androguard.core.bytecodes.jvm import *
from androguard.core.bytecodes.dvm import *
from androguard.core.bytecodes.apk import *
from androguard.core.analysis.analysis import *

# Find mergeFrom() method in class with name cn
def find_mergeFrom(dvm, cn):
    l = filter(lambda m: m.get_name() == "mergeFrom" and not m.get_descriptor().endswith("MessageMicro;"), dvm.get_methods_class(cn))
    if (len(l) != 1):
        raise Exception("Unable to find mergeFrom() in class %s" % cn)
    return l[0]

def index_basic_blocks(dvm, vma, cn):
    m = find_mergeFrom(dvm, cn)
    ma = vma.get_method(m)
    bbs = ma.basic_blocks.gets()

    # Find the basic block which ends with a sparse-switch (usually the first)
    l = filter(lambda bb: bb.get_instructions()[-1].get_name() == "sparse-switch", bbs)
    if (len(l) != 1):
        return {} # TODO
        # raise Exception("Unable to find a basic block ending with a sparse-switch in mergeFrom() method of class %s" % cn)
        # TODO handle packed-switch (cf 1ere classe dans proto_class_names)
    ss = l[0]

    # Get the offset of the sparse-switch, and the sparse-switch-payload
    # instruction.
    n = ss.get_nb_instructions()
    offset_ss = sum(i.get_length() for i in ss.get_instructions()[:n-1])
    ssp = ss.get_special_ins(offset_ss)

    # Fill the list {key: bb} for this class
    d = {}
    for key, target in zip(ssp.get_keys(), ssp.get_targets()):
        d[key >> 3] = ma.basic_blocks.get_basic_block(offset_ss + target*2)

    return d

def get_invoked_method_info(i):
    m = i.cm.get_method_ref(i.BBBB)
    return (m.get_class_name(), m.get_name(), m.get_descriptor())

def classname_to_messagename(cn):
    return cn.split('/')[-1].replace(';', '')

def ulfirst(s):
    return s[0].lower() + s[1:]

def analyse_bb(bb, k, cn):
    message_type = None
    l = []

    # Index all invoke-virtual instructions. There should be 2 per basic block;
    # one for reading from the stream, the other for setting the appropriate
    # class member.
    for i in bb.get_instructions():
        n = i.get_name()
        if n == "invoke-virtual":
            icn, imn, imd = get_invoked_method_info(i)
            l.append( imn ) # class name : icn.split("/")[-1]

        if n == "invoke-direct":
            icn, imn, _ = get_invoked_method_info(i)

            if (imn == "<init>"):
                message_type = classname_to_messagename(icn)


    if (len(l) == 0): # no calls, probably the switch basic block. skip it.
        return None

    if (len(l) != 2):
        raise Exception("There are %d invoke-virtual calls in this basic block, wtf is this shit?!" % len(l)) # TODO

    if (not l[0].startswith("read")):
        raise Exception("The first invoke-virtual call is not a readXXX(), dafuq?")

    typ = l[0][4:].lower()
    method = l[1]
    field = method[3:]

    if (typ == "message"):
        typ = message_type

    if (method.startswith("set")):    # optional (or required?) # TODO
        return (field, typ, "optional")

    if (method.startswith("add")):    # repeated
        return (field, typ, "repeated")

##############################################################
# Main program starts here
##############################################################

if (len(sys.argv) != 2):
    print "Usage: %s <apk>" % sys.argv[0]
    print "Tries to recover the .proto file used by the given APK."
    print "Works only with Micro-Protobuf apps, and has only been tested with Google Play."
    print "For more information: http://www.segmentationfault.fr/publications/reversing-google-play-and-micro-protobuf-applications/"
    print
    sys.exit(0)

apk = APK(sys.argv[1])
dvm = DalvikVMFormat(apk.get_dex())
vma = uVMAnalysis(dvm)

proto_classes = filter(lambda c: "MessageMicro;" in c.get_superclassname(), dvm.get_classes())
if (len(proto_classes) == 0):
    print "Unable to find protobuf micro classes."
    sys.exit(0)

proto_class_names = map(lambda c: c.get_name(), proto_classes)

"""
cn = proto_class_names[1]
print cn
pprint([(i.split('/')[-1], sorted([(k >> 3) for k in index_basic_blocks(dvm, vma, i).keys()])) for i in proto_class_names])
"""

messages_info = {}
for pcn in proto_class_names:
    mn = classname_to_messagename(pcn)
    d = {}
    for (k, bb) in index_basic_blocks(dvm, vma, pcn).items():
        info = analyse_bb(bb, k, pcn)
        if (info is not None):
            d[k] = info
    messages_info[mn] = d
#pprint(messages_info)

def treeify(seq):
    """Resolve message dependencies
    http://stackoverflow.com/questions/3464975/how-to-efficiently-merge-multiple-list-of-different-length-into-a-tree-dictonary
    """
    ret = {}
    for path in seq:
        cur = ret
        for node in path:
            cur = cur.setdefault(node, {})
    return ret

messages_dep = treeify([k.split('$') for k in messages_info])
#pprint(messages_dep)

def print_proto(d, parent = (), indent=0):
    """Display all protos"""
    for m, sd in sorted(d.items(), cmp=lambda x,y: cmp(x[0],y[0])):
        full_name_l = parent+(m,)
        full_name = '$'.join(full_name_l)

        is_message_or_group = full_name in messages_info

        if (is_message_or_group):
            print_message(m, sd, parent, indent)
        else:
            print_proto(sd, full_name_l, indent)


def print_message(name, sd, parent, indent, title="message", extras=[]):
    full_name_l = parent+(name,)
    full_name = '$'.join(full_name_l)

    #if (messages_printed[full_name]):         # TODO useless
    #    return False

    # messages_printed[full_name] = True

    if (title == "message"):
        print indent*"    " + "message %s {" % (name)
    else:
        print indent*"    " + "%s group %s = %d {" % (extras[0], name, extras[1])

    i = indent+1
    infos = messages_info[full_name]

    # Display sub-messages, except groups
    groups = [field for (field, typ, _) in infos.values() if typ == 'group']
    print_proto(dict([(k, m) for (k, m) in sd.items() if k not in groups]), full_name_l, i)

    for k, info in sorted(infos.items(), cmp=lambda x,y: cmp(x[0],y[0])):
        field, typ, rule = info

        if (typ == 'group'):
            print_message(field, sd[field], full_name_l, i, "group", (rule, k))
        else:
            print '    '*i + ' '.join([rule, typ.split('$')[-1], ulfirst(field)]) + ' = %d;' % k

    print indent*"    " + "}"

print_proto(messages_dep)

