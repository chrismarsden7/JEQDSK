import json
from json import JSONEncoder
import numpy as np
from freeqdsk import geqdsk
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import jsbeautifier

class NumpyArrayEncoder(JSONEncoder):
    '''
    JSONEncoder that handles numpy data types.
    '''

    def default(self, obj):

        # Numpy arrays
        if isinstance(obj, np.ndarray):

            return obj.tolist()
        
        # Numpy integers
        if isinstance(obj, np.int64):

            return int(obj)
        
        # Numpy floats
        if isinstance(obj, np.float64):

            return float(obj)
        
        return JSONEncoder.default(self, obj)

def read(path):
    '''
    Reads a .jeqdsk file and returns a dict of its contents.

    Inputs:
    -------

    path - str, path to read the jeqdsk, './example.jeqdsk'

    Returns:
    --------

    data - dict
    '''

    # Open the jeqdsk file
    with open(path,'r') as f:

        # Load its contents
        data = json.load(f)

    # Close the jeqdsk file
    f.close()

    # Convert the 1D pprime, ffprime, q, fpol and pres data into numpy arrays
    data['pprime'] = np.asarray(data['pprime'])
    data['ffprime'] = np.asarray(data['ffprime'])
    data['qpsi'] = np.asarray(data['qpsi'])
    data['fpol'] = np.asarray(data['fpol'])
    data['pres'] = np.asarray(data['pres'])

    # Convert the 2D psi grid into a numpy array
    data['psi'] = np.asarray(data['psi'])

    # Returns its contents
    return data

def write(path,data,encoder=NumpyArrayEncoder):
    '''
    Creates a .jeqdsk file.

    Inputs:
    -------

    path - str, path to write the jeqdsk, './example.jeqdsk'
    data - dict
    encoder - JSONEncoder, a suitable default is provided.

    Returns:
    --------

    '''

    # Open the output file
    with open(path,'w+') as f:

        # Set the indent size
        options = jsbeautifier.default_options()
        options.indent_size = 2

        # Create the jsonified output as a string, and beautify it
        out_str = jsbeautifier.beautify(json.dumps(data,cls=encoder), options)

        # Write the json string to the output file
        f.write(out_str)

    # Close the file
    f.close()

def display_contents(data):
    '''
    Prints to console the key, value pairs of items in a dict.

    Inputs:
    -------

    data - dict

    Returns:
    --------

    '''

    # Loop through key, value pairs in the dict
    for key, val in data.items():

        # Print key
        print(key)

        # Print value
        print(val)

        # Line break
        print('')

def plot_data(data):
    '''
    Creates a graphical representation of the equilibrium data.
    '''

    # Create a figure and GridSpec
    fig = plt.figure(constrained_layout=True)
    gs = GridSpec(ncols=3,nrows=3,figure=fig)

    # Create axes for plotting
    ax_eq = fig.add_subplot(gs[:,0])
    ax_pprime = fig.add_subplot(gs[0,1])
    ax_ffprime = fig.add_subplot(gs[1,1])
    ax_q = fig.add_subplot(gs[2,1])
    ax_fpol = fig.add_subplot(gs[0,2])
    ax_pres = fig.add_subplot(gs[1,2])

    # Add a GridSpec within a GridSpec
    gs2 = gs[2,2].subgridspec(nrows=1,ncols=2)
    ax_text_left = fig.add_subplot(gs2[0,0])
    ax_text_right = fig.add_subplot(gs2[0,1])

    # Pull relevant data from the data dict
    rleft = data['rleft']
    rdim = data['rdim']
    nx = data['nx']
    zmid = data['zmid']
    zdim = data['zdim']
    ny = data['ny']
    psi = data['psi']
    sibdry = data['sibdry']
    rbdry = data['rbdry']
    zbdry = data['zbdry']
    rlim = data['rlim']
    zlim = data['zlim']
    pprime = data['pprime']
    ffprime = data['ffprime']
    q = data['qpsi']
    fpol = data['fpol']
    pres = data['pres']
    rcentr = data['rcentr']
    rmagx = data['rmagx']
    zmagx = data['zmagx']
    simagx = data['zmagx']
    bcentr = data['bcentr']
    cpasma = data['cpasma']

    # Calculate the 1D R, Z of the equilibrium
    R = np.linspace(rleft,rleft+rdim,nx,endpoint=True)
    Z = np.linspace(zmid-0.5*zdim,zmid+0.5*zdim,ny,endpoint=True)

    # Plot the poloidal cross section of the plasma incl limiters
    ax_eq.contour(R,Z,psi.T,levels=50)
    ax_eq.contour(R,Z,psi.T,levels=[sibdry],colors='r')
    ax_eq.plot(rmagx,zmagx,'rx')
    ax_eq.plot(rbdry,zbdry,'yx')
    ax_eq.plot(rlim,zlim,'k')
    ax_eq.set_aspect('equal')
    ax_eq.set_xlabel('R (m)')
    ax_eq.set_ylabel('Z (m)')

    # Calculate the 1D psiN
    psiN = np.linspace(0.0,1.0,nx,endpoint=True)

    # Plot the 1D pprime, ffprime, q, fpol and pres profiles
    ax_pprime.plot(psiN,pprime)
    ax_pprime.set_xlabel(r'$\psi_{N}$')
    ax_pprime.set_ylabel(r'pprime($\psi_{N}$) Pa Wb rad$^{-1}$')

    ax_ffprime.plot(psiN,ffprime)
    ax_ffprime.set_xlabel(r'$\psi_{N}$')
    ax_ffprime.set_ylabel(r'ffprime($\psi_{N}$) m $^{2}$ T $^{2}$ Wb rad$^{-1}$')

    ax_q.plot(psiN,q)
    ax_q.set_xlabel(r'$\psi_{N}$')
    ax_q.set_ylabel(r'q($\psi_{N}$)')

    ax_fpol.plot(psiN,fpol)
    ax_fpol.set_xlabel(r'$\psi_{N}$')
    ax_fpol.set_ylabel(r'fpol($\psi_{N}$) m T')

    ax_pres.plot(psiN,pres)
    ax_pres.set_xlabel(r'$\psi_{N}$')
    ax_pres.set_ylabel(r'pressure($\psi_{N}$) Pa')

    # Create strings detailing plasma parameters
    text_left = ''
    text_left += r'$n_{x}$: ' + str(nx) +'\n'
    text_left += r'$n_{y}$: ' + str(ny) +'\n'
    text_left += r'$r_{dim}$: ' + str(rdim) +'\n'
    text_left += r'$z_{dim}$: ' + str(zdim) +'\n'
    text_left += r'$r_{centr}$: ' + str(rcentr) +'\n'
    text_left += r'$r_{left}$: ' + str(rleft) +'\n'
    text_left += r'$z_{mid}$: ' + str(zmid)
    ax_text_left.text(0.0,0.0,text_left,fontsize=14)

    text_right = ''
    text_right += r'$r_{magx}$: ' + str(rmagx) +'\n'
    text_right += r'$z_{magx}$: ' + str(zmagx) +'\n'
    text_right += r'$si_{magx}$: ' + str(simagx) +'\n'
    text_right += r'$si_{bdry}$: ' + str(sibdry) +'\n'
    text_right += r'$b_{centr}$: ' + str(bcentr) +'\n'
    text_right += r'$c_{pasma}$: ' + str(cpasma)
    ax_text_right.text(0.0,0.0,text_right,fontsize=14)

    # Hide the axes for these subplots
    ax_text_left.set_axis_off()
    ax_text_right.set_axis_off()

    plt.show()

def read_first_line_geqdsk(fp):
    '''
    Reads the first line of a GEQDSK

    Inputs:
    fp - Filehander for the GEQDSK being read

    Returns:

    '''
    fp.seek(0)
    lines = fp.readlines()
    first_line = lines[0]

    print(first_line)

    # Get the label
    find_label = True
    found_first_label_char = False
    i = 0
    while find_label:
        
        char = first_line[i]

        if char == ' ' and not found_first_label_char:
            i += 1

        elif char != ' ' and not found_first_label_char:
            found_first_label_char = True
            start_label = i
            i += 1

        elif char != ' ' and found_first_label_char:
            i += 1

        else:
            end_label = i - 1
            label = first_line[start_label:end_label+1]
            find_label = False

    # Get the date
    find_date = True
    i = end_label + 1
    found_first_date_char = False
    while find_date:

        char = first_line[i]

        if char ==' ' and not found_first_date_char:
            i += 1

        elif char != ' ' and not found_first_date_char:
            found_first_date_char = True
            start_date = i
            i += 1

        elif char != ' ' and found_first_date_char:
            i += 1

        else:
            end_date = i - 1
            date = first_line[start_date:end_date+1]
            find_date = False

    # Now find the shot number. This is somewhere to the right of the # symbol
    # and may or may not be separated by spaces.
    hash_pos = first_line.rfind('#')
    find_shot = True
    i = hash_pos + 1
    found_first_shot_char = False
    while find_shot:

        char = first_line[i]

        if char == ' ' and not found_first_shot_char:
            i += 1

        elif char!=' ' and not found_first_shot_char:
            found_first_shot_char = True
            start_shot = i
            i += 1

        elif char != ' ' and found_first_shot_char:
            i += 1

        else:
            end_shot = i - 1
            shot = first_line[start_shot:end_shot+1]
            find_shot = False

    # Now find the time. This is expressed by an integer to the right of
    # the shot number, separated by some spaces, and ends with 'ms'. It may
    # be that there is a space between the time and the units, and it may be
    # that the units are in 's'. All of these are handled.
    find_time = True
    i = end_shot + 1
    found_first_time_char = False
    while find_time:

        char = first_line[i]

        if char == ' ' and not found_first_time_char:
            i += 1

        elif char!=' ' and not found_first_time_char:
            found_first_time_char = True
            start_time = i
            i += 1

        elif char!= (' ' or 'm' or 's') and found_first_time_char:
            i += 1

        else:
            end_time= i - 1
            time = first_line[start_time:start_time+1]
            find_time = False

    print(label)
    print(date)
    print(shot)
    print(time)
    

def convert_geqdsk_to_jeqdsk(path_g,path_j):
    '''
    Converts a geqdsk to a jeqdsk

    Inputs:
    -------
    
    path_g - str, path to read geqdsk, './example.geqdsk'
    path_j - str, path to write jeqdsk, './example.jeqdsk'

    Returns:
    --------

    '''

    # Open the geqdsk
    with open(path_g,'r') as f:
    
        # Read its contents
        data = geqdsk.read(f)

        # At present the FreeQDSK GEQDSK reader does not extract data from
        # the first line. This is performed below
        read_first_line_geqdsk(f)

    # Close the geqdsk
    f.close()

    # Write the jeqdsk
    write(path_j,data)

def convert_jeqdsk_to_geqdsk(path_g,path_j):
    '''
    Converts a jeqdsk to a geqdsk

    Inputs:
    -------
    
    path_g - str, path to write geqdsk, './example.geqdsk'
    path_j - str, path to read jeqdsk, './example.jeqdsk'

    Returns:
    --------

    '''

    # Read the jeqdsk
    data = read(path_j)

    # Open the geqdsk
    with open(path_g,'w+') as f:
    
        # Write data to the file
        geqdsk.write(data,f)

    # Close the geqdsk
    f.close()

if __name__ == '__main__':

    # Read the example d3d jeqdsk and display its contents.

    data = read('../../data/diiid.jeqdsk')

    display_contents(data)

    plot_data(data)

    # Convert the example jeqdsk to a new geqdsk
    convert_jeqdsk_to_geqdsk('../../data/diiid_new.geqdsk','../../data/diiid.jeqdsk')

    # Convert the example geqdsk to a new jeqdsk
    convert_geqdsk_to_jeqdsk('../../data/diiid.geqdsk','../../data/diiid_new.jeqdsk')