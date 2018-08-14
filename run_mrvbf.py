# Import the module
import os
import subprocess

paths = ['MDE', 'OUT', 'OUT/MRVBF', 'OUT/MRRTF']


for i in paths:
    print("Making {} folder".format(i))
    try:
        os.mkdir(i)
    except:
        pass


def import_data(saga_cmd, mde_loc):
    print("Importando datos...")
    saga_lib = 'io_gdal'
    saga_tool = '0'
    mde_out = '-GRIDS=./MDE/mde180'
    mde_in = '-FILES={}'.format(mde_loc)
    trf = '-TRANSFORM 1'
    command = [saga_cmd, saga_lib, saga_tool, mde_out, mde_in, trf]
    print(command)
    p1 = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = p1.communicate()[0]
    print(p1)


def run_mrvbf(saga_cmd):
    print("Calculando MRVBF...")
    # Set up the echo command and direct the output to a pipe

    saga_lib = 'ta_morphometry'  # Saga Library Analysis

    saga_tool = '8'  # Saga Tool of library

    mde_par = '-DEM=./MDE/mde180.sgrd'
    mrvbf_out = '-MRVBF=./OUT/MRVBF/mrvbf'
    mrrtf_out = '-MRRTF=./OUT/MRRTF/mrrtf'
    t_slope = '-T_SLOPE=7'
    t_pctl_v = '-T_PCTL_V=0.2'
    t_pctl_r = '-T_PCTL_R=0.1'
    p_slope = '-P_SLOPE=4'
    p_pctl = '-P_PCTL=3'
    update = '-UPDATE=1'
    classify = '-CLASSIFY=0'
    max_res = '-MAX_RES=100'
    command = [saga_cmd, saga_lib, saga_tool, mde_par, mrvbf_out, mrrtf_out,
               t_slope, t_pctl_v, t_pctl_r, p_slope, p_pctl, update, classify,
               max_res]
    print(command)
    p1 = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = p1.communicate()[0]
    print(output)


def export_data(saga_cmd, out_grid):
    print("Exportando datos...")
    saga_lib = 'io_gdal'
    saga_tool = '2'
    mde_out = '-GRIDS={}'.format(out_grid)
    name_tif = os.path.basename(out_grid)[0:-5] + '.tif'
    out_tif = '-FILES={}'.format(name_tif)
    command = [saga_cmd, saga_lib, saga_tool, mde_out, out_tif]
    print(command)
    p1 = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = p1.communicate()[0]
    print("###########################################################")
    print("########################   FIN   ##########################")
    print("###########################################################")


if __name__ == "__main__":
    saga_cmd = 'saga_cmd'   # Saga Executable
    mde_loc = 'MDE180.tif'   # MDE location
    import_data(saga_cmd, mde_loc)
    run_mrvbf(saga_cmd)
    outs = [r'./OUT/MRVBF/mrvbf.sgrd', r'./OUT/MRRTF/mrrtf.sgrd']
    for i in outs:
        export_data(saga_cmd, i)
