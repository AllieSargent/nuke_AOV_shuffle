Overview:
This script will recognize AOV layers from a render, shuffle out the passes, and recombine them with denoise nodes added based on a users input

Note that this script should work with most common renderers but is primarily implemented for Arnold renders.


The UI allows the user to add a denoise node to the network for a given pass.



How to Download and install:

To install, download the file above
- In Nuke open the script editor by right-clicking the panels window
in the dropdown navigate to window --> script editor.
- Import the file via the load a script button
- Run the script with a render selected

The script will automatically add itself to your nuke custom panels menu


How to Use:

1. Select a node
2. Run the script
3. If you want the option to add denoise or delete layers (recommended)
select show channels
4. Select channel to denoise with enumerate box and delete with delete buttons
5. Select shuffle to create an AOV layout


Features:

- Interactive GUI for Denoise

- Easy Layer Pass Removal

- Includes Copy to Maintain Alpha


Logic:

Parsing the AOVs layers coming in from a selected node, the script will create dot, shuffle, and merge nodes unique to each layer that will connect
to the previously created node. If a GUI dropdown box is changed to denoise the corresponding dictionary key to that layer will change to true and
a denoise node will the added to the layout. If the delete button is pressed for a given layer the layer will be removed from the set that a for
loop runs through for each pass making the layout.
