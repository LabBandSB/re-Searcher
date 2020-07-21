import re
from itertools import chain
import pandas as pd

#gets header line and its index
def get_header(input_vcf, samples):
    meta = []
    column_names = []
    header_index = 0

    with open(input_vcf, 'r') as vcf:  
        for line in vcf:
            if '##' in line:
                header_index += 1 
                meta.append(line.strip())
            elif '#CHROM' in line:
                column_names.extend(line.strip().split('\t'))

    #extract main columns and user-input sample columns only
    if samples: 
        samples_list = []

        for sample in samples:
            if sample in column_names:
                samples_list.append(sample)
            else:
                print(f'{sample} was not found. Try again!')

        #Modify columns names
        try:
            Format = column_names.index('FORMAT')
            column_names = column_names[:Format + 1]
            column_names.extend(samples_list)
        except ValueError:
            print('Your VCF header is invalid, fix column names')

    return meta, column_names, header_index
    
def get_filter(df, output_vcf, samples, keywords, passfail, chrom, pos):
    for chunk in df:
        if chrom:
            chrom = [str(i) for i in chrom_parse(chrom)]
            chunk = chunk[chunk['#CHROM'].str.contains(f"^chr[{'|'.join(chrom)}]$|^[{'|'.join(chrom)}]$", case = False, regex = True)]

        if pos:
            range_pos, row_pos = pos_parse(pos)
            df_empty = pd.DataFrame()
            for i in range_pos:
                df_empty = df_empty.append(chunk[(chunk['POS'] >= int(i[0])) & (chunk['POS'] <= int(i[1]))]) 
            for i in row_pos:
                df_empty = df_empty.append(chunk[chunk['POS'] == int(i)])
            chunk = df_empty

        if keywords:        
            chunk = chunk[chunk.apply(lambda r: r.str.contains('|'.join(keywords), case = False).any(), axis = 1)]

        if passfail:
            chunk = chunk[chunk['FILTER'].str.contains(passfail, case = False)]

        chunk.to_csv(output_vcf, mode='a', sep='\t', index=False, header = False) # writes chunks to a new vcf

#Genotype conversion
def number_gt_to_letter_gt(input_vcf, column_names):
    CHROM = column_names.index('#CHROM')
    output = []
    with open(input_vcf) as f:
        for line in f:
            if '#' in line: #skip lines with '#'
                pass
            elif 'GT' in line: #parse only lines with 'chr'
                arr = line.strip().split('\t')

                if len(arr[CHROM + 3]) > 1 or len(arr[CHROM + 4]) > 1:
                    multi = '\t'.join(arr)
                    continue

                arr[CHROM + 8] = 'GT' #edit FORMAT to GT
                
                ra = '\t'.join(arr[0:CHROM + 9])
                sample_gt = list()
                for gt in arr[CHROM + 9:]:
                    gt = gt.split(':')[0]
                    if len(arr[CHROM + 3]) > 1 or len(arr[CHROM + 4]) > 1:
                        letter_gt = 'MULTIALLELIC SNP' #If more that 1 nucleotide in a field
                    elif gt == '0/0' or gt == '0|0':
                        letter_gt = (arr[CHROM + 3]) * 2 #if 0/0 GT -> REF/REF
                    elif gt == '0/1' or gt == '0|1':
                        letter_gt = (arr[CHROM + 3]) + (arr[CHROM + 4]) #if 0/1 GT -> REF/ALT
                    elif gt == '1/1' or gt == '1|1':
                        letter_gt = (arr[CHROM + 4]) * 2 #if 1/1 GT -> ALT/ALT
                    elif gt == './.':
                        letter_gt = '..'
                    sample_gt.append(letter_gt)
                sample_gt = '\t'.join(sample_gt)
                output.append(ra + '\t' + sample_gt + '\n')
                
            else: pass

    return output, multi
# function searches samples, extract them and merge with main columns
def read_vcf(input_vcf, header_index, column_names, chunksize = 10 ** 6):
    return pd.read_csv(input_vcf, header = header_index, usecols = column_names, sep = '\t', chunksize = 10 ** 6, low_memory = False, dtype = {'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str, 'QUAL': str, 'FILTER': str, 'INFO': str})
   
def write_vcf(output_vcf, meta, column_names, nometa, array=[]):
    with open(output_vcf, 'w') as w:
        if nometa is True:
            w.write('\t'.join(column_names))
        else:
            w.write('\n'.join(meta) + '\n' + '\t'.join(column_names))
        if array != []: 
            w.write('\n')
            for line in array:
                w.write(line)
 
def write_multi(output_vcf, column_names, multi = []):
    with open(output_vcf, 'w') as w:
        if multi != []:
            w.write('\t'.join(column_names))
            w.write('\n')
            for line in multi:
                w.write(line)
                
#Parse range of chromosomes from command line        
def chrom_parse(rgstr):
    def parse_range(rg):
        if len(rg) == 0: return []
        parts = re.split( r'[:-]', rg)
        if int(parts[0]) > int(parts[1]) or len(parts) > 2:
           raise ValueError("Invalid range: {}".format(rg))
        try:
            return range(int(parts[0]), int(parts[-1])+1)
        except ValueError:
            if len(parts) == 1:
                return parts
            else:
                raise ValueError("Non-integer range: {}".format(rg))
    rg = map(parse_range, re.split("\s*[,;]\s*", rgstr))
    return list(set(chain.from_iterable(rg)))

#Parse range of positions from command line   
def pos_parse(posstr): 
    range_pos = []
    row_pos = []

    pos = re.split("\s*[,;]\s*", posstr)
    
    for p in pos:
        if '-' in p or ':' in p:
            rg = re.split( r'[:-]', p)
            if len(rg) == 2:
                range_pos.append(rg)
            else: 
                raise ValueError('Invalid range')
        else:
            row_pos.append(p)

    #check if row_pos between range_pos        
    for row in row_pos:
        for rg in range_pos:
            if int(rg[1]) <= int(rg[0]):
                raise ValueError('Invalid range')

            if int(row) >= int(rg[0]) and int(row) <= int(rg[1]):
                row_pos.remove(row)
   
    return range_pos, row_pos

##################
##################    
if __name__ == "__main__":
    pass
