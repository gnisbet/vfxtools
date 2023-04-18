import os
import hou
import glob
import shutil
import warnings

from pxr import Sdf, Usd, UsdGeom

def repath_textures(texture, folder):
    '''
    The folder path to the textures, and the folder you want to save it in
    '''
    files = [texture[1:-1]]
    if "UDIM" in texture:
        files = find_udims(texture)

    copy_textures(files, folder)
    return "{}/{}".format(folder, os.path.basename(texture))

def copy_textures(files, folder):

    if not os.path.exists(folder):
        os.makedirs(folder)
    for file in files:
        copy_path = "{}/{}".format(folder, os.path.basename(file))
        if not os.path.exists(copy_path):
            if os.path.exists(file):
                print("Copying {} to {}".format(file, copy_path))
                shutil.copy(file, copy_path)
            else:
                warnings.warn("This file doesn't exist:\n{}".format(file))

def find_udims(udim):
    path = udim.replace("<UDIM>", "*")
    path = path[1:-1] 
    return glob.glob(path)

def main():
    node = hou.pwd()
    print("\n-- ###### --\nCleaning the log\n-- ###### --\n")

    # Get paths to all shader nodes
    ls = hou.LopSelectionRule()
    base_path = "/"
    ls.setPathPattern('{0}** & %type:Shader'.format(base_path))
    paths = ls.expandedPaths(node.inputs()[0])
    stage = node.editableStage()
    usd_path = node.input(0).evalParm("filepath1")
    texture_dir = "{}/export/textures".format(os.path.dirname(usd_path))
    for path in paths:
        prim = stage.GetPrimAtPath(path)
        attrs = prim.GetAttributes()
        for attr in attrs:
            value = attr.Get()
            if (type(value) is Sdf.AssetPath):
                texture_path = str(value)
                if not texture_path.startswith("@opdef"):
                    path = repath_textures(texture_path, texture_dir)
                    attr.Set(Sdf.AssetPath(path[:-1]))
                else:
                    warnings.warn("This texture is defined in the scene:\n{}".format(texture_path))

main()
