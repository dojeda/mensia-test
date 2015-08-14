#!/usr/bin/env python3

import re
import os.path
import pandas as pd

class FileParserHelper:

    def __init__(self):
        '''Create a parser object to read Mensia's data sets

        Extracts group G, subject X and time T from files named
        groupG/subjectX_T.csv

        Extracts features vs electrodes from the file contents
        '''
        self.regexp = re.compile(r'^.*/' +
                                 r'group(?P<group>[0-9]+)/' +
                                 r'subject(?P<subject>[0-9]+)_' +
                                 r'(?P<time>[0-9]+).csv$')

    def parse(self, filename):
        "Returns the parsed information from filename as a dict"
        result = self.regexp.match(filename)
        if not result:
            return {}
        else:
            return result.groupdict()

    def extract_data(self, filename):
        "Extract features and columns from a csv file"
        # Extract information from filename
        extras = self.parse(filename)
        if not extras:
            # Early stop when it's not the right kind of file
            return None
        print('Reading',filename)

        # Read CSV data and rename columns accordingly
        df = pd.read_csv(filename,header=None,sep=';')
        assert(df.shape[1] == 10)
        df.columns = ['O1','O2','Oz','Cz','C3','C4','Fz','F8','F7','Fpz']
        df['feature'] = ['ft-{}'.format(i) for i in range(df.shape[0])]

        # Add individual,group,time information
        for key in extras:
            df[key] = extras[key]

        return df

def main():

    dataPath = os.path.join(os.path.abspath('.'),'data')
    outputFile = os.path.join(os.path.abspath('.'),'data','full_data.csv')
    parser = FileParserHelper()
    full_df = None

    print('Searching in',dataPath)
    for root, dirs, files in os.walk(dataPath):
        for f in files:
            fullpath = os.path.join(root,f)
            df = parser.extract_data(fullpath)
            if df is None: continue
            if full_df is None:
                full_df = df
            else:
                full_df = full_df.append(df,ignore_index=True)

    if full_df is not None:
        full_df.to_csv(outputFile)

if __name__ == '__main__':
    main()
