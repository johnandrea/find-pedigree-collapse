@echo off

if exist r.err del r.err

find-pedigree-collapse.py --iditem=refn --personid 1 cousins-plus.ged >cousins-plus.out 2>>r.err 
find-pedigree-collapse.py --iditem=refn --personid 1 half-cousins.ged >half-cousins.out 2>>r.err
find-pedigree-collapse.py --iditem=refn --personid 1 multiple-plus.ged >multiple-plus.out 2>>r.err
find-pedigree-collapse.py --iditem=refn --personid 1 sibling-child.ged >sibling-child.out 2>>r.err

find-pedigree-collapse.py --dates --iditem=refn --personid 1 charles-ii-of-spain.ged  >charles-ii-of-spain.out 2>>r.err

find-pedigree-collapse.py --dates --iditem=refn --personid 5 british-royals-2023.ged  >british-royals-2023.out 2>>r.err
