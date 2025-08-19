import os
import re
import glob
import hiero
from hiero.core import TrackItem

from PySide2.QtWidgets import QMessageBox
from PySide2.QtCore import Qt

# Inputs
# show = "ta"
#step = "layout"
#variant = "slap-array"

def get_filepath_dict(filepath):
    fp_dict = dict()
    splits = filepath.split("/")
    fp_dict["shot"] = splits[5]
    fp_dict["step"] = splits[6]
    return(fp_dict)

def find_latest_mov(base_dir):
    version_pattern = re.compile(r'v(\d{3})')
    versions = []

    # Find version folders (e.g., v001, v023, v108)
    if not os.path.exists(base_dir):
        return None
    for name in os.listdir(base_dir):
        full_path = os.path.join(base_dir, name)
        if os.path.isdir(full_path):
            match = version_pattern.fullmatch(name)
            if match:
                versions.append((int(match.group(1)), full_path))

    if not versions:
        print("No version folders found.")
        return None

    # Get highest version
    latest_version = max(versions, key=lambda x: x[0])[1]

    # Look inside its 'mov' subfolder for a .mov file
    mov_dir = os.path.join(latest_version, "mov")
    if not os.path.isdir(mov_dir):
        print(f"No 'mov' folder in {latest_version}")
        return None

    for file in os.listdir(mov_dir):
        if file.lower().endswith(".mov"):
            return os.path.join(mov_dir, file)

    print(f"No .mov file found in {mov_dir}")
    return None

def latest_child_folder(parent_dir, pattern="*"):
    # Build search pattern for child folders
    search_path = os.path.join(parent_dir, pattern)
    
    # Get all matching paths that are directories
    folders = [f for f in glob.glob(search_path) if os.path.isdir(f)]
    
    if not folders:
        return None  # No matching folder
    
    # Find the most recently modified folder
    latest = max(folders, key=os.path.getmtime)
    return latest

def print_update(old_path, new_path):
    old_file = os.path.basename(old_path)
    new_file = os.path.basename(new_path)
    print(f"Replaced: {old_file}\nwith: {new_file}\n")

def display_update(message_dict, step):

    # data = {"Shot": "sh010", "Version": "v003", "Artist": "Gary"}

    data = message_dict

    # Build HTML table
    html = "<table border='1' cellspacing='0' cellpadding='3' padding='3'>"

    count = 0

    for key, value in data.items():
        if(count==0):
            html += f"<tr><td><b>{key}</b></td><td><b>{value}</b></td></tr>"
        else:
            key = key
            base_split = os.path.splitext(value)
            if(base_split):
                if(base_split[1].endswith("mov")):
                    spl = base_split[0].split("-")
                    value = f"{spl[4]}_{spl[5]}_{spl[6]}"
            html += f"<tr><td>{key}</td><td>{value}</td></tr>"
        count += 1
    html += "</table>"

    msg = QMessageBox()
    msg.setWindowTitle(f"{step.title()} Edit Updates")
    msg.setTextFormat(Qt.RichText)  # enable HTML
    msg.setText(html)
    msg.setStandardButtons(QMessageBox.Ok)

    # Set the window width (and optional height)
    # msg.setFixedWidth(400)   # adjust as needed
    msg.resize(750, 200)   # alternative if you want both width + height

    msg.exec_()

    # QMessageBox.information(None, "Details", html)


def run(steps=["comp"], vncs=["main-comp"], replace=False):

    message_dict = {"Shot" : "Update"}

    seq = hiero.ui.activeSequence()

    if not seq:
        raise Warning("Please select a sequence")

    # Getting selection
    te = hiero.ui.getTimelineEditor(seq) # Can specify any sequence as argument
    track_items = te.selection() # Return currently selected items in timeline

    for count, step in enumerate(steps):

        if not (replace):
            new_track = hiero.core.VideoTrack(step)
            seq.addTrack(new_track)

        vnc = vncs[count]
        step = step.lower()

        for track_item in track_items:
            clip = track_item.source()
            rn = clip.readNode()
            filepath = rn.metadata()["input/filename"]
            shot = get_filepath_dict(filepath)["shot"]
            step_root = f"/mnt/jobs/{show}/shots/{shot}/{step}/versions/image/"
            root = latest_child_folder(step_root, pattern=vnc)
            if not root:
                message_dict[shot] = "No mov"
                print(f'There are no {step} versions in {shot} that match {vnc}')
                continue
            mov = find_latest_mov(root)
            if(mov):
                if(replace and filepath!=mov):
                    track_item.replaceClips(mov)
                    print_update(filepath, mov)
                    
                    message_dict[shot] = os.path.basename(mov)

                elif(replace):
                    path = os.path.basename(root)
                    print(f"{shot} already has the latest {path} from {step}\n")

                    message_dict[shot] = "None"
                    
                if not replace:
                    # Create a new TrackItem from the source clip
                    new_track_item = hiero.core.TrackItem(track_item.name(), track_item.mediaType())
                    new_track_item.setSource(clip)

                    # Copy timing
                    new_track_item.setTimelineIn(track_item.timelineIn())
                    new_track_item.setTimelineOut(track_item.timelineOut())
                    new_track_item.setSourceIn(track_item.sourceIn())
                    new_track_item.setSourceOut(track_item.sourceOut())

                    # Add to the new track
                    new_track.addItem(new_track_item)

                    new_track_item.replaceClips(mov)

                    print(f"\nAdded {os.path.basename(mov)} to {step.title()}")

                    message_dict[shot] = os.path.basename(mov)
            else:
                message_dict[shot] = "No mov"
                print(f"{shot} has no mov file")

    display_update(message_dict, step)
    # QMessageBox.information(None, "Finished", "This is an information popup.")

# print(show, step, variant_component)

run(steps=steps, vncs=variant_component, replace=replace)

'''
# Getting 'current' item
cv = hiero.ui.currentViewer()
seq.trackItemAt(cv.time()) # Return topmost track item under playhead
seq.trackItemsAt(cv.time()) # Return enabled tracks at specified time from top to bottom, defaults to video
seq.trackItemsAt(cv.time(), TrackItem.MediaType.kAudio) # Same as above but returns audio tracks instead
''' 

'''
import os
import sys
import importlib

path = "/mnt/jobs/ta/documents/gprysbet/dev/"
if path not in sys.path: sys.path.append(path)

import hiero_replace_clips as hrc
importlib.reload(hrc)

hrc.run()
'''

'''
script_path = "/mnt/jobs/ta/documents/gprysbet/dev/hiero_replace_clips.py"

with open(script_path, "r") as f:
    script_code = f.read()

variables = {
    "passed_name": "Gary",
    "show" : "test"
}

exec(script_code, variables)
'''