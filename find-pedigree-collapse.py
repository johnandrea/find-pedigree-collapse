#!/usr/bin/python3

"""
?

No support provided.
"""

import sys
import argparse
import importlib.util
import os


def get_version():
    return '0.6'


def load_my_module( module_name, relative_path ):
    """
    Load a module in my own single .py file. Requires Python 3.6+
    Give the name of the module, not the file name.
    Give the path to the module relative to the calling program.
    Requires:
        import importlib.util
        import os
    Use like this:
        readgedcom = load_my_module( 'readgedcom', '../libs' )
        data = readgedcom.read_file( input-file )
    """
    assert isinstance( module_name, str ), 'Non-string passed as module name'
    assert isinstance( relative_path, str ), 'Non-string passed as relative path'

    file_path = os.path.dirname( os.path.realpath( __file__ ) )
    file_path += os.path.sep + relative_path
    file_path += os.path.sep + module_name + '.py'

    assert os.path.isfile( file_path ), 'Module file not found at ' + str(file_path)

    module_spec = importlib.util.spec_from_file_location( module_name, file_path )
    my_module = importlib.util.module_from_spec( module_spec )
    module_spec.loader.exec_module( my_module )

    return my_module


def get_program_options():
    results = dict()

    results['infile'] = None
    results['personid'] = None
    results['iditem'] = 'xref'
    results['dates'] = False
    results['libpath'] = '.'

    arg_help = 'Find cross branch parents.'
    parser = argparse.ArgumentParser( description=arg_help )

    arg_help = 'Show version then exit.'
    parser.add_argument( '--version', action='version', version=get_version() )

    arg_help = 'Id for the person chosen for ancestors or descendents.'
    parser.add_argument( '--personid', type=str, help=arg_help )

    arg_help = 'How to find the person. Default is the gedcom id "xref".'
    arg_help += ' Othewise choose "exid", "refn", etc.'
    parser.add_argument( '--iditem', default=results['iditem'], type=str, help=arg_help )

    arg_help = 'Show dates along with the names.'
    parser.add_argument( '--dates', default=results['dates'], action='store_true', help=arg_help )

    # maybe this should be changed to have a type which better matched a directory
    arg_help = 'Location of the gedcom library. Default is current directory.'
    parser.add_argument( '--libpath', default=results['libpath'], type=str, help=arg_help )

    parser.add_argument('infile', type=argparse.FileType('r') )

    args = parser.parse_args()

    results['personid'] = args.personid
    results['iditem'] = args.iditem.lower()
    results['dates'] = args.dates
    results['infile'] = args.infile.name
    results['libpath'] = args.libpath

    return results


def get_indi_years( indi ):
    # return ( birth - death ) or (birth-) or (-death)
    # but None if both dates are empty

    def get_indi_year( indi_data, tag ):
        # "best" year for birth, death, ...
        # or an empty string
        result = ''

        best = 0
        if readgedcom.BEST_EVENT_KEY in indi_data:
           if tag in indi_data[readgedcom.BEST_EVENT_KEY]:
              best = indi_data[readgedcom.BEST_EVENT_KEY][tag]
        if tag in indi_data:
           if indi_data[tag][best]['date']['is_known']:
              result = str( indi_data[tag][best]['date']['min']['year'] )
        return result

    result = None

    birth = get_indi_year( data[ikey][indi], 'birt' ).strip()
    death = get_indi_year( data[ikey][indi], 'deat' ).strip()
    if birth or death:
       result = '(' + birth +'-'+ death + ')'

    return result


def get_name( indi ):
    result = 'none'

    if indi is not None:
       result = data[ikey][indi]['name'][0]['value']
       if readgedcom.UNKNOWN_NAME in result:
          # change to word with no special characters
          result = 'unknown'
       else:
          if options['dates']:
             dates = get_indi_years( indi )
             if dates:
                result += dates

    return result.replace( '/', '' )


def get_fam_names( fam ):
    result = ''
    sep = ''
    for parent in ['husb','wife']:
        name = 'unknown'
        if parent in data[fkey][fam]:
           name = get_name( data[fkey][fam][parent][0] )
        result += sep + name
        sep = '\n + '
    return result


def find_person( person, item ):
    # it is possible that the selected person is not found
    result = None

    if item == 'xref':
       # ensure the person lookup is the same as what it used in gedcom
       # if given  5  change to  @I5@
       person = 'i' + person.lower()
       person = '@' + person.replace( 'ii', 'i' ) + '@'
       person = person.replace( '@@', '@' )

       for indi in data[ikey]:
           rec_no = data[ikey][indi]['file_record']['index']
           rec_key = data[ikey][indi]['file_record']['key']
           if person == data[rec_key][rec_no]['tag'].lower():
              result = indi
              break

    else:
       found = readgedcom.find_individuals( data, item, person )
       if found:
          # just take the first one
          result = found[0]

    return result


def find_parents( indi ):
    # for the input person
    # return [ fam, parent1, parent2 ]
    # or [ fam, parent ] or [], i/e. empty if none
    results = []
    key = 'famc'
    if key in data[ikey][indi]:
       fam = data[ikey][indi][key][0]
       results.append( fam )
       for parent in ['husb','wife']:
           if parent in data[fkey][fam]:
              results.append( data[fkey][fam][parent][0] )
    return results


def build_tree( indi ):
    global ancestor_families

    parent_family = find_parents( indi )

    if parent_family:
       fam = parent_family[0]

       if fam in ancestor_families:
          print( get_fam_names(fam) )

       else:
          ancestor_families.append( fam )

          for parent in parent_family[1:]:
              build_tree( parent )


options = get_program_options()

readgedcom = load_my_module( 'readgedcom', options['libpath'] )

ikey = readgedcom.PARSED_INDI
fkey = readgedcom.PARSED_FAM

opts = dict()
opts['only-birth'] = True
opts['exit-on-no-families'] = True
opts['exit-on-no-individuals'] = True

data = readgedcom.read_file( options['infile'], opts )

ancestor_families = []

start = find_person( options['personid'], options['iditem'] )

if start:
   print( 'Start with:' )
   print( get_name(start) )
   print( '' )
   print( 'Pedigree collapse:' )
   print( '' )
   build_tree( start )

else:
   print( 'No start person found', file=sys.stderr )
   sys.exit(1)
