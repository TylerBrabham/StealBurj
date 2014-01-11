-- Every time the program is run it takes an input .dxf file and an output file name, which 
needs to have no extension. The program will output two files, one a .m script that will 
generate the corresponding structure in FEDEASLab, and another a .brj file, a proprietary
file for the StealBurj program.

-- An additional input is the "-m" flag, which indicates to StealBurj that the user wants 
to modify an existing .brj file using another .dxf file. For the case of Steel Bridge, the
assumption is that the user wants to replace one layer in the .brj file with a new layer 
from the .dxf file, while leaving all other layers in tact. This allows the user to save
all the element properties in the current .brj file.

-- Considering using as input just a .m file, not a .brj file. Then there is no need to 
have a proprietary file format. Just need to make a new parser that can take as input 
a .m file and create all the corresponding connections and element data.