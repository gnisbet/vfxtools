import os
import shutil
from fnmatch import fnmatch
def GetUsdData(filePath):

    from pxr import Sdf
    return Sdf.Layer.FindOrOpen(filePath)

def GetFiles(root, pattern):

    filepaths = []

    for path, subdirs, files in os.walk(root):

        for name in files:

            filepath = os.path.join(path, name)

            if fnmatch(filepath, pattern):

                filepaths.append(filepath)

    return filepaths
def FixSlashes(filepaths, backup = False, debug = False):

    for path in filepaths:

        # Get usd data
        data = GetUsdData(path)

        filedata = data.ExportToString()

        o_filedata = filedata
        # Replace the target string
        filedata = filedata.replace('/', '\\')

        backup_file = "{}.backup".format(path)

        if debug:

            if (o_filedata != filedata):

                print("### ------------------------- ###\n")

                print("Slashes would be changed in: {}".format(path))

                if (backup==True):

                    print("File will be backed up here: {}".format(backup_file))

        else:         

            if (o_filedata != filedata):

                if (backup==True):

                    # Backup file
                    shutil.copyfile(path, backup_file)

                # Write the file out again
                with open(path, 'w') as file:

                    file.write(filedata)

                print("Fixed slashes in: {}".format(path))

root = r"N:\dalston\publish\assets\Character\trishA"
pattern = "*\MOD\*.usd"
filepaths = GetFiles(root, pattern)

FixSlashes(filepaths, backup=True, debug=True)