import sys
import struct
import bpy
from bpy.types import Operator
import math

def load_str(file):
    bytes = b''
    b = file.read(1)
    while not b == b'\x00':
        bytes += b
        b = file.read(1)
    return bytes.decode("utf-8")

model_path = r"C:/Users/gnisb/Downloads/mp_lobby_S20/_models/"
mprt_file = r"C:/Users/gnisb/Downloads/mp_lobby_S20/mp_lobby_LOD0.mprt"

model_path = r"C:/Users/gnisb/Downloads/mp_rr_desertlands_mu4/_models/"
mprt_file = r"C:/Users/gnisb/Downloads/mp_rr_desertlands_mu4/mp_rr_desertlands_mu4_LOD0.mprt"

model_path = r"C:/Users/gnisb/Downloads/mp_rr_desertlands_mu1/_models/"
mprt_file = r"C:/Users/gnisb/Downloads/mp_rr_desertlands_mu1/mp_rr_desertlands_mu1_LOD0.mprt"


file = open(bpy.path.abspath(mprt_file), "rb")
header = struct.unpack("3I", file.read(0xC))

# Setup Defaults

scene = bpy.context.scene.props
NameList = []
posList = []
rotList = []
scaleList = []
filter = ["godrays"]
# filter = ((scene.filter).replace(" ", "")).split(",")
# radius = scene.radius
radius = 10000
# filter_keep = ["terrain"]
coordinates = scene.coordinates

# Import mprt

for i in range(header[2]):
    name = load_str(file)
    fpos = file.tell()
    posrotscale = struct.unpack("7f", file.read(0x1C))
    # XYZ, XYZW
    skip = False
    modPos = (posrotscale[0], posrotscale[1], posrotscale[2])
    if filter[0] != '':
        for x in filter:
            if x in name:
                skip = True
    # if filter_keep[0] != '':
    #     for x in filter_keep:
    #         if x not in name:
    #             skip = True
    if radius != 0:
        distance = math.dist(coordinates,modPos)
        if distance > radius:
            skip = True
    if skip == False:
        scaleList.append((posrotscale[6],posrotscale[6],posrotscale[6]))
        posList.append((posrotscale[0], posrotscale[1], posrotscale[2]))
        rotList.append((math.radians(posrotscale[3]), math.radians(posrotscale[4]), math.radians(posrotscale[5])))
        NameList.append(name)
    # progress = (i/((header[2])-1))
    # sys.stdout.write("\r{0} ▌{1}▐ {2}% \r".format("Parsing mprt...", "█"*(int(round(50*progress))) + "#"*(50-(int(round(50*progress)))), round(progress*100,2)))
    # sys.stdout.flush()
print("Finished parsing mprt file")

# Create object list

ObjectList=(list(dict.fromkeys(NameList)))
print(ObjectList)
AssetCollection = bpy.data.collections.new("Assets")
bpy.context.scene.collection.children.link(AssetCollection)
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[AssetCollection.name]
collections = {}

for i in range(len(ObjectList)):
    AName = ObjectList[i]
    progress = (i/((len(ObjectList))-1))
    sys.stdout.write("Importing... ({0}%) {1}...\n".format(round(progress*100,2),AName))
    print("1")
    model_filepath = bpy.path.abspath(model_path + "%s/%s_LOD0.cast" % (AName,AName))
    print(model_filepath)
    bpy.ops.import_scene.cast(filepath = model_filepath)
    print("2")
    if os.path.isfile(bpy.path.abspath(model_path + "%s/%s_LOD0.cast" % (AName,AName))) == False:
        print('Error, missing file %s.cast' % (AName))
        PlaceholderCol = bpy.data.collections.new(AName)
        AssetCollection.children.link(PlaceholderCol)
    print("3")
    collections[AName] = bpy.context.view_layer.active_layer_collection.collection.children[-1]

bpy.context.view_layer.layer_collection.children[AssetCollection.name].exclude = True    
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection
MapCollection = bpy.data.collections.new("Map")

for i in range(len(NameList)):
    obj = bpy.data.objects.new(NameList[i], None)
    bpy.data.collections[MapCollection.name].objects.link(obj)
    obj.instance_type = 'COLLECTION'
    obj.instance_collection = collections[NameList[i]]
    #obj.rotation_mode = 'QUATERNION'
    obj.location = posList[i]
    obj.scale = scaleList[i]
    #obj.rotation_quaternion = rotList[i]
    obj.rotation_euler = rotList[i]
    #obj.rotation_mode = 'XYZ'
    progress = (i/((len(NameList))-1))
    sys.stdout.write("{0} ▌{1}▐ {2}% \r".format("Instancing...", "█"*(int(round(50*progress))) + "#"*(50-(int(round(50*progress)))), round(progress*100,2)))
    sys.stdout.flush()

bpy.context.scene.collection.children.link(MapCollection)
print('\nFinished!')