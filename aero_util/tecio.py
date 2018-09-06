''' Routines for reading/writing data from Tecplot files '''

import io
import logging
import numpy as np
import shlex
import re

log = logging.getLogger(__name__)

_TECPLOT_KEYWORDS = [
    'TITLE',     'FILETYPE',      'VARIABLES',       'ZONE',        'TEXT',
    'GEOMETRY',  'CUSTOMLABELS',  'DATASETAUXDATA',  'VARAUXDATA',
]

# Keep it simple for now. Just return list(dict(str:np.array))
# Only supporting structured grids with nodal data for now

#----------------------------------------------------------------------------
# Public API Functions
#----------------------------------------------------------------------------
def read_dat(path_or_file, *args, **kwargs):
    ''' Top level routine to load data '''
    if not isinstance(path_or_file, io.TextIOBase):
        with open(path_or_file) as f:
            zones = _read_dat_impl(f, *args, **kwargs)
    else:
        zones = _read_dat_impl(f, *args, **kwargs)
    return zones


#----------------------------------------------------------------------------
# Internal Implementation Functions
#----------------------------------------------------------------------------
def _read_dat_impl(f, *args, **kwargs):
    ''' Reads Tecplot file data into a list of dicts '''
    zones = []
    varnames = None
    for first_word in _peek_line(f):
        first_word = first_word.upper()
        if first_word == 'VARIABLES':
            varnames = _read_variables(f)
        elif first_word == 'ZONE':
            zones.append(_read_zone(f,varnames))
        else:
            if first_word in _TECPLOT_KEYWORDS:
                log.info('Ignoring "%s" record.', first_word)
            f.readline()
    return zones

def _read_variables(f):
    ''' Parse tecplot "variables" record.
        File pointer must be positioned at the start of the "VARIABLES" keyword.
    '''
    record = f.readline().split('=', maxsplit=1)[1]  # Remove 'VARIABLES ='
    for first_word in _peek_line(f):
        first_word = first_word.upper()
        if first_word in _TECPLOT_KEYWORDS:
            break
        else:
            record += f.readline()
    variables = shlex.split(record)
    log.info('Read variable names %s from file header', variables)
    return variables

def _read_zone(f,varnames=None):
    ''' Parser tecplot "zone" record.
        File pointer must be positioned at the start of the "ZONE" keyword.
    '''
    # TODO: Process/check VARLOCATION. Currently assume all variables are nodal.
    options = _read_zone_options(f)

    # If no varnames, try to infer from first line of data
    if not varnames:
        assert options['DATAPACKING'] == 'POINT', \
            'Data must be in point format if variable names are omitted.'
        position = f.tell()
        line = f.readline()
        f.seek(position)
        varnames = [f'V{i}' for i in range(len(line.split()))]
    nvars = len(varnames)

    # Warnings/consistnecy checks
    assert options['ZONETYPE'] == 'ORDERED', 'This function only supports ordered zones'
    if options['DT'] and not all([dt == 'DOUBLE' for dt in options['DT']]):
        log.warning('Converting all variable data to double precision')

    # Load all the data for this zone
    npts = options['I'] * options['J'] * options['K']
    data = np.fromfile(f, count=npts*nvars, sep=' ')
    if options['DATAPACKING'] == 'POINT':
        data = data.reshape((nvars, options['I'], options['J'], options['K']), order='F')
        vardata = [np.squeeze(data[i,:,:,:]) for i in range(nvars)]
    else:
        data = data.reshape((options['I'], options['J'], options['K'], nvars), order='F')
        vardata = [np.squeeze(data[:,:,:,i]) for i in range(nvars)]

    return dict(zip(varnames,vardata))

def _read_zone_options(f):
    ''' Parse options from zone header '''

    # Get all lines of the zone header
    header = f.readline().split(maxsplit=1)[1]  # Remove "ZONE" keyword
    for first_word in _peek_line(f):
        if first_word[0] in '123456890+-.':
            break
        else:
            header += f.readline()

    # Split the header in to key-value pairs
    tokens  = [ s.strip().upper() for s in re.split(',?\s*(\w+)\s*=', header.strip()) ]
    options = dict(zip(tokens[1::2],tokens[2::2])) # tokens[0] is alway empty string

    # Do clean up on options we acutally use (dequote, coerce types, etc.)
    options['T']  = _remove_delimiters(options.get('T',''))
    options['I']  = int(options.get('I',1))
    options['J']  = int(options.get('J',1))
    options['K']  = int(options.get('K',1))
    options['DT'] = _remove_delimiters(options.get('DT','DOUBLE')).split()
    options['ZONETYPE'] = _remove_delimiters(options.get('ZONETYPE','ORDERED'))
    options['DATAPACKING'] = _remove_delimiters(options.get('DATAPACKING','BLOCK'))

    return options


#----------------------------------------------------------------------------
# Low Level Helper Function
#----------------------------------------------------------------------------
def _peek_line(f):
    ''' Yield first word each non-blank line of a file w/o advancing file pointer.
        Note: If you read from a file after peeking, the next word yielded
              by the generator will be the first word after the end of the read.
              Thus, if your read terminated mid-line, the word yielded will not
              be the first word of the next line.
    '''
    position = f.tell()
    for line in iter(f.readline, ''):
        line = line.strip()
        if line:
            first_word = re.split('[ =]', line, maxsplit=1)[0]
            f.seek(position)
            yield first_word
        position = f.tell()

def _remove_delimiters(s, delim='"\'()[]'):
    ''' Removes delimiters from start and end of string '''
    # This is a bit overzealous and will remove non-matching delimeters
    # However, not really a concern for this application
    if s and s[0] in delim and s[-1] in delim:
        return s[1:-1]
    else:
        return s



