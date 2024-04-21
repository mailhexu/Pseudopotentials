import os
import glob
from ase.data import chemical_symbols
import shutil

root = '/home/hexu/projects/dojo/pseudo_dojo-master/pseudo_dojo/pseudos'
elems = chemical_symbols[57:72]
"""
for i in Co N C O H
do
oncvpspr.x < $i.in
cp ONCVPSPPSML $i.psml
done
"""


def find_input(elem, xc):
    epath = f"ONCVPSP-{xc}-PDv0.4/{elem}"
    path = os.path.join(root, epath)
    if not os.path.exists(path):
        return []
    else:
        return glob.glob(f"{root}/{epath}/{elem}*.in")


def get_input_sp(xc, elem, label="-sp.in"):
    epath = f"ONCVPSP-{xc}-PDv0.4/{elem}"
    fname = f"{root}/{epath}/{elem}{label}"
    if os.path.exists(fname):
        return fname

def replace_word(fname, old, new):
    with open(fname, 'r') as f:
        lines = f.readlines()
    with open(fname, 'w') as f:
        for line in lines:
            f.write(line.replace(old, new))


def gen_psml(xc, elem, label="-sp.in", rel='SR', output_path='pps'):
    command = {'NR': 'oncvpspnr.x', 'SR': 'oncvpsp.x', "FR": 'oncvpspr.x'}
    cache_path = os.path.join(root, 'cache', xc, elem)
    os.makedirs(cache_path, exist_ok=True)
    fname = get_input_sp(xc, elem, label)
    if fname is not None:
        replace_word(fname, 'psp8', f"upf")
    path_nr = os.path.join(root, output_path, f"{xc}_{rel}")
    os.makedirs(path_nr, exist_ok=True)
    failed = open("failed.txt", 'w')
    if fname is not None:
        shutil.copy(fname, cache_path)
        os.chdir(cache_path)
        os.system("rm ./*")
        os.system(f"{command[rel]} < {fname} > output")
        name = os.path.join(path_nr, f"{elem}.psml")
        print(os.path.join(path_nr, f"{elem}.psml"))
        psml_fname = os.path.join(cache_path, "ONCVPSPPSML")
        if os.path.exists(psml_fname):
            shutil.copy(psml_fname,
                        os.path.join(path_nr, f"{elem}.psml"))
            shutil.copy(os.path.join(cache_path, "output"),
                        os.path.join(path_nr, f"{elem}.out"))
        else:
            failed.write(f"{name}\n")
            print(f"{name}: Failed")

    failed.close()


def gen_all_fincore():
    for xc in ['PBE', 'PBEsol', 'PW']:
        for elem in elems:
            gen_psml(xc, elem, rel='NR', label='3+_f-in-core.in',
                     output_path='pps_fincore')
            gen_psml(xc, elem, rel='SR', label='3+_f-in-core.in',
                     output_path='pps_fincore')
            gen_psml(xc, elem, rel='FR', label='3+_f-in-core.in',
                     output_path='pps_fincore')

def gen_all_withf():
    for xc in ['PBE', 'PBEsol', 'PW']:
        for elem in elems:
            #gen_psml(xc, elem, rel='NR', label='_sp.in',
            #         output_path='withf')
            #gen_psml(xc, elem, rel='SR', label='_sp.in',
            #         output_path='withf')
            gen_psml(xc, elem, rel='FR', label='_sp.in',
                     output_path='withf')
    


def get_psml(elem, xc):
    cache_path = os.path.join(root, 'cache', xc, elem)
    os.makedirs(cache_path, exist_ok=True)
    # shutil.copy(src=os.path.)


def test():
    xc = "PBE"
    for elem in elems:
        inputs = find_input(elem, xc)
        for inp in inputs:
            get_psml(elem, xc)


# test()
gen_all_withf()
