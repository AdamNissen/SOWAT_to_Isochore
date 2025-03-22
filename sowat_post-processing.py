# -*- coding: utf-8 -*-
"""
Processing script for sowat produced .txt files. All isochore points are saved
into a single .xlsx spreadsheet. Summary data from the isochore files can 
also be saved into a second sheet in that .xlsx file.

Note, two variables in the main() function dictate which data gets read, and 
where it gets saved. For further iterations change both input_folder and 
output_file 
"""

import pandas as pd


def concat_isochores(path, save_summary = True):
    """
    A function for batch processing isochore files produced by Dr. Thomas Driesners
    sowat executable file. All of the files have to have a .txt suffix, this is
    not automatically done by sowat, but the .txt suffix does not (seem to) change
    the contents of these files. This function also targets every text file in a
    repository/folder. 

    Parameters
    ----------
    path : string, folderpath
        Full path to the folder containing the isochore.txt files that are to be 
        concatenated. e.g. C:/data/isochores
    save_summary : boolean, default = True
        Whether to save the additional summary information (viz. temperature of
        total homogeniztion, pressure of total homogenization, salinity, density)
        for each fluid inclusion from its isochore.txt file. The default is True.

    Returns
    -------
    None.

    """
    
    # Collecting all of the .txt filepaths in the folder into a list using glob
    import glob
    files = []
    for x in glob.glob(path+'/*.txt'):
        x = x.replace('\\', "/")
        files.append(x)
    
    #Establishing the output dataframes
    isochores = pd.DataFrame(columns = ['Inclusion Code',
                                        'Sample',
                                        'Assemblage',
                                        'Inclusion'
                                        'T (C)',
                                        'P (bar)'])
    summary = pd.DataFrame(columns = ['Inclusion',
                                      'Temperature of total homogenization (C)',
                                      'Pressure of total homogenization (bar)',
                                      'Salinity (wt% NaCl eq.)',
                                      'Density (g/ccm)' ])
    
    #For loop iterates over the list of .txt files
    for x in files:
        name = x.replace(path+'/', '')
        name = name.replace('.txt', '')
        print(name + " initiated")
        #Using open to create a temporary variable "file" that is the open file
        #No need to call file.close() when using "with open()"
        with open(x, 'r') as file:
            text = file.readlines()[0:-1] #Extracting the text from the document into a list of lines
            PT_pairs = text[8:-1]
            #For loop fills the isochores dataframe with the PT data line by line
            for y in PT_pairs:
                t, p = y.split()
                t = float(t) #altered to float to avoid text/number error
                p = float(p)
                newline = {'Inclusion_code': [name],
                           'Sample': [name.split('_')[0]],
                           'Assemblage': [name.split('_')[1].split('-')[0]],
                           'Inclusion': [name.split('-')[1]],
                           'T (C)': [t],
                           'P (bar)': [p]}
                isochores = pd.concat([isochores, pd.DataFrame.from_dict(newline)], ignore_index = True)

            T = float(text[1].split()[5]) #Saved as float to avoid text number error 
            P = float(text[2].split()[5])
            S = float(text[3].split()[2])
            D = float(text[4].split()[2])
            newline = {'Inclusion': name,
                       'Temperature of total homogenization (C)': [T], 
                       'Pressure of total homogenization (bar)': [P],
                       'Salinity (wt% NaCl eq.)': [S],
                       'Density (g/ccm)': [D]}
            summary = pd.concat([summary, pd.DataFrame.from_dict(newline)], ignore_index = True)
        print(name + " completed")
    if save_summary == True:
        return isochores, summary
    else:
        return isochores
    


if __name__ == "__main__":
    input_folder = "Data/sowat_raw"

    # #input_folder = "D:/Fluid inclusions/SOWAT_isochores/sowat_raw"
    output_file = "Output/all_isochores.xlsx"
    data, summary = concat_isochores(path = input_folder)
    writer = pd.ExcelWriter(output_file)
    data.to_excel(writer, sheet_name = "isochores", index = False)
    summary.to_excel(writer, sheet_name = "summary data", index = False)
    writer.close()


