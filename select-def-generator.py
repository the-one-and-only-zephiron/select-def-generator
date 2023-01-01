import os

# Set the directories you want to search
characters_directory = "chars"
stages_directory = "stages"
data_directory = "data"

# Get a list of all the subdirectories in the "chars" directory
characters = [d for d in os.listdir(characters_directory) if os.path.isdir(os.path.join(characters_directory, d))]

# Get a list of all the .def files in the "stages" directory
stages = [f for f in os.listdir(stages_directory) if f.endswith(".def")]

# Check if the "select.def" file exists in the "data" directory
select_def_path = os.path.join(data_directory, "select.def")
if not os.path.exists(select_def_path):
    print("The 'select.def' file does not exist in the 'data' directory.")
else:
    # Open the "select.def" file and read its contents
    with open(select_def_path, "r") as f:
        lines = f.readlines()

    # Find the indices of the lines that contain the ";STARTCHAR" and ";ENDCHAR" strings
    start_char_index = None
    end_char_index = None
    for i, line in enumerate(lines):
        if ";STARTCHAR" in line:
            start_char_index = i
        elif ";ENDCHAR" in line:
            end_char_index = i
            break
    
    # If both indices are found, delete the lines between them (inclusive)
    if start_char_index is not None and end_char_index is not None:
        del lines[start_char_index:end_char_index+1]

    # Insert the subdirectories between the ";STARTCHAR" and ";ENDCHAR" lines
    lines.insert(start_char_index, ";STARTCHAR\n")
    for character in characters:
        lines.insert(start_char_index+1, character+"\n")
    lines.insert(start_char_index+1+len(characters), ";ENDCHAR\n")
    
# Find the indices of the lines that contain the ";STARTSTAGE" and ";ENDSTAGE" strings
start_stage_index = None
end_stage_index = None
for i, line in enumerate(lines):
    if ";STARTSTAGE" in line:
        start_stage_index = i
    elif ";ENDSTAGE" in line:
        end_stage_index = i
        break

# If both indices are found, delete the lines between them (inclusive)
if start_stage_index is not None and end_stage_index is not None:
    del lines[start_stage_index:end_stage_index+1]

# Insert the .def files between the ";STARTSTAGE" and ";ENDSTAGE" lines, with a "stages/" prefix
lines.insert(start_stage_index, ";STARTSTAGE\n")
for stage in stages:
    lines.insert(start_stage_index+1, "stages/"+stage+"\n")
lines.insert(start_stage_index+1+len(stages), ";ENDSTAGE\n")


# Make a backup of the "select.def" file
backup_path = select_def_path + ".bak"
with open(select_def_path, "r") as f_in, open(backup_path, "w") as f_out:
    f_out.write(f_in.read())

# Open the "select.def" file in write mode and write the modified contents to it
with open(select_def_path, "w") as f:
    f.writelines(lines)

# Print the names of the subdirectories and .def files
print("chars added:")
for character in characters:
    print(character)

print("stages added:")
for stage in stages:
    print(stage)
