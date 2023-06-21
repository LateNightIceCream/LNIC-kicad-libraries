# LNIC-kicad-libraries
kicad libraries!

## Components
For a list of components see [here](https://github.com/LateNightIceCream/LNIC-kicad-libraries/blob/main/component_list.md).

## Conventions

For conventions used see the official [KiCad Library Conventions](https://klc.kicad.org/).

### Exceptions
#### 3D Models
- F9.3 violation: no `${KICAD6_3DMODEL_DIR}/` prefix for the model path, as this is not supposed to be committed to the official kicad libs

## Installation
### 3D Model Path
Kicad currently (6.0.10) does not support relative 3D-Paths and the "3D-Search-Path" seems to be undocumented.

To have the footprints include the 3D models from this library you have to add an environment variable called `KICAD_LIB_LNIC_DIR` with the absolute path to the library on your system.

1. Preferences -> Configure Paths
2. Click the add (+) button in the Environment Variable section
3. Enter `KICAD_LIB_LNIC_DIR` as the name
4. Click inside the Path text field, then on the folder icon and choose the library folder (src)
