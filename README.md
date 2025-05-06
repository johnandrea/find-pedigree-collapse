# find-pedigree-collapse
Read a genealogy GEDCOM file and display the families where pedigree collapse occurs

## Options ##

--version

Display version number then exit.

--personid= <id value>
  
The id of the person to select for output. Used in combination with the iditem option.
By default this is the the individual xref in the gedcom file and so may be given as for example
as @i42@ or I42 or just 42.

--iditem=  xref or user specified such as EXID, REFNUM, etc.
  
The tag in the gedcom file used to match the specified person. Default is xref which is the gedcom individual identifier.
  When using a non-xref tag, the given personid value must match exactly the value in the gedcom file. The match makes
  use of the readgedcom function find_individuals so an id name such as birth.date may be used or for a custom event such as
  event.extraref If more than one match is found the first (unordered) one is taken.
  
--dates
  
Include birth and death years with the names.
  
--libpath=directory-containing-readgedcom

Location containing the readgedcom.py library file. The path is relative to the program being used. An absolute path will not work. Default is the same location as the program (".").

## Usage ##

find-pedigree-collapse.py --iditem=refn --personid 5 family.ged >found-collapse.out

No output after the line "Pedigree collapse:" indicates that none was found.

## Installation ##

- Requires python 3.6+
- Copy Python file
- also requires gedcom library [readgedcom.py](https://github.com/johnandrea/readgedcom) in the same directory, or in a location specified by the libpath option.

