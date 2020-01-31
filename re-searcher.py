#!/usr/bin/env python3
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import io
import pandas as pd
import os
import time
from datetime import datetime


#Function for logging
def time_it(f):
    time_it.active = 0

    def tt(*args, **kwargs):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        time_it.active += 1
        t0 = time.time()
        tabs = '\t'*(time_it.active - 1)
        name = f.__name__
        log_file = open(r"logfile.log", "a") #creates logfile.log text file
        log_file.write('{data} {tabs}Executing <{name}> \n'.format(data=dt_string, tabs=tabs, name=name))
        res = f(*args, **kwargs)
        log_file.write('{tabs}Function <{name}> execution time: {time:.3f} seconds \n'.format(
            tabs=tabs, name=name, time=time.time() - t0))
        time_it.active -= 1
        log_file.close()
        return res
    return tt
#
file = ''
path = ''
head = ''
key = ''
root = Tk()

#'help' submenu
def getting_started():
    os.startfile('Getting started.txt')
def about():
    os.startfile('About.txt')

#Dropdown menu
menubar = Menu(root)
root.config(menu=menubar)
subMenu = Menu(menubar, tearoff=0) #submenu
menubar.add_cascade(label='Help', menu=subMenu)
subMenu.add_command(label='Getting Started', command=getting_started)
subMenu.add_command(label='About', command=about)

#root
root.minsize(200, 155) #size
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.title('re-Searcher') #title
#root.iconbitmap('logo.ico') #logo

#
# Top frame
#
frame = Frame(root, bg='#334660', bd=1, relief='sunken')
frame.grid(row=0, column=0, sticky='news')
frame.grid_columnconfigure(0, weight=1)
#
# Function to store vcf file path
@time_it
def open_file():
    global path
    path = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                      filetypes=(("vcf files", "*.txt .vcf"), ("all files", "*.*")))
    try:
        if path:
            entry_path.delete(0, END)  # Remove current text in entry
            entry_path.insert(0, path)  # Insert the 'path'
            statusbar['text'] = 'The file was found and opened'
        else:
            messagebox.showinfo("Cancel", "Oops! You clicked Cancel")
            statusbar['text'] = 'Oops, find a file again'
    except IOError:
        messagebox.showinfo("Error", "Could not open a file")
#
# File path entry
entry_path = Entry(frame, width=70)
entry_path.insert(0, 'File directory')
entry_path.grid(row=0, column=0, sticky='news', padx=6, pady=3)

#
# Browse file button
button_path = Button(frame, text='Browse', bg='#c1c7cf', fg='black', relief='ridge', command=open_file)
button_path.grid(row=0, column=1, sticky='news', padx=6, pady=3)

#
# Header columns name get
@time_it
def get_header_line(file):
    n = 0 #calculating header for row
    for line in open(file):
        n += 1
        if '#CHROM' in line:
            line = line.strip().split('\t')
            break
    return line, n

# Meta-lines get with '##'
def get_meta(file):
    arr=list()
    for line in open(file):
        if '##' in line:
            arr+=[line]
    return arr

# Header extraction
@time_it
def header_save():
    head, n = get_header_line(path)
    try:
        if '#CHROM' in head:
            filename = filedialog.asksaveasfilename(title="Select file", defaultextension='.vcf', filetypes=[("vcf files", ".vcf")])
            save_search_result(filename, head=head)
            statusbar['text'] = 'The header was extracted'
        else:
            statusbar['text'] = 'The header was not extracted, try again'
    except TypeError:
        messagebox.showinfo("Error", "Wrong file, try again")
        statusbar['text'] = 'The header was not extracted, try again'

# Header extraction button
button_header = Button(frame, text='Extract Header', bg='#c1c7cf', fg='black', relief='ridge', command=header_save)
button_header.grid(row=0, column=2, sticky='news', padx=6, pady=3)


# Keyword function that binds to button
@time_it
def keyword_button():
    global key, head
    if keyword.get():
        word = [i.strip() for i in keyword.get().split(',')]
        total_count = len(word)
        arr, keyword_list, count = keyword_search(path, word)
        head, n = get_header_line(path)
        meta=get_meta(path)
        filename = filedialog.asksaveasfilename(title="Select file", defaultextension='.vcf', filetypes=[("vcf files", ".vcf")])
        statusbar['text'] = '{} occurrences of {} keywords in the file were found'.format(count, total_count)
        save_search_result(filename, arr, meta=meta, head=head)
    else:
        messagebox.showinfo("Oops!", "Type a keyword")

# Searches keywords in vcf
def keyword_search(file, keyword_list):
    arr = list()
    count_keywords = 0
    with open(file) as f:
        for line in f:
            if '#' in line:
                pass
            else:
                line = line.strip().split('\t')
                for keyword in keyword_list:
                    for word in line:
                        if keyword == word:
                            line = '\t'.join(line) + '\n'
                            arr +=[line]
                            count_keywords += 1
    return arr, keyword_list, count_keywords


# Keyword entry
keyword = StringVar()
entry_keyword = Entry(frame, textvariable=keyword, width=70)
entry_keyword.insert(0, 'Keywords')
entry_keyword.grid(row=1, column=0, sticky='news', padx=6, pady=3)

# Keyword button
button_keyword = Button(frame, text='Extract', bg='#c1c7cf', fg='black', relief='ridge', command=keyword_button)
button_keyword.grid(row=1, column=1, sticky='news', padx=6, pady=3)

# Function that binds with button to search keywords from txt
@time_it
def keyword_file_button():
    path_keywords = filedialog.askopenfilename(initialdir="/", title="Select A File With Keywords",
                                      filetypes=(("vcf files", "*.txt .vcf"), ("all  files", "*.*")))
    head, n = get_header_line(path)
    meta=get_meta(path)
    arr, keys, count_keywords = keyword_file(path_keywords, path)
    total_count = len(keys)
    filename = filedialog.asksaveasfilename(title="Select file", defaultextension='.vcf', filetypes=[("vcf files", ".vcf")])
    statusbar['text'] = '{} occurrences of {} keywords in the file were found'.format(count_keywords, total_count)
    save_search_result(filename, arr, meta=meta, head=head)

# Extract keywords list from txt with keywords
def keyword_file(keyword_file, file):
    with open(keyword_file, 'r') as f:
        keyword_list = [line.strip()for line in f for line in line.split(',')]
        arr, keys, count_keywords = keyword_search(file, keyword_list)
    return arr, keys, count_keywords

# Button to search keywords from txt
button_keyword_file = Button(frame, text='Extract from File', bg='#c1c7cf', fg='black', relief='ridge',
                                 command=keyword_file_button)
button_keyword_file.grid(row=1, column=2, sticky='news', padx=6, pady=3)

# Saves search result (meta-lines, header and body)
def save_search_result(file, arr='', meta='', head=''):
    with open(file, 'w') as f:
        if meta:
            meta = ''.join(meta)
            f.write(meta)
        if head:
            head = '\t'.join(head) + '\n'
            f.write(head)
        for line in arr:
            f.write(line)
    f.close()
#
# Function that binds to button, execute sample search function and saves result
@time_it
def sample_button():
    if sample.get():
        samples = [i.strip() for i in sample.get().split(',')]
        save = filedialog.asksaveasfilename(title="Select file", defaultextension='.vcf',
                                                filetypes=[("vcf files", ".vcf")])
        sample_search(path, samples, save)
        #
        #total_count = len(samples)
        #statusbar['text'] = '{} samples out of {} input samples in the file were found'.format(count, total_count)
    else:
        messagebox.showinfo("Oops!", "Type a sample name")

# function searches samples, extract them and merge with main columns
def read_vcf(path, head_index, usecols, chunksize=10**3):
    return pd.read_csv(path, header=head_index-1, usecols=usecols, sep='\t', chunksize=10**3, low_memory=False, dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str, 'QUAL': str, 'FILTER': str, 'INFO': str})

# find main columns
def main_columns():
    cols, head_index = get_header_line(path)
    main_columns = []
    for value in cols:
        main_columns.append(value)
        if value == 'FORMAT':
            break
    return main_columns, head_index

#sample search function
def sample_search(path, samples, save):
    df_main, head_index = main_columns() #main column names and index of header line
    usecols = df_main+samples #main columns and user input sample columns
    df = read_vcf(path, head_index, usecols) #reads file
    meta = get_meta(path) #meta-lines
    head = df_main+samples #header line
    try:
        if save:
            save_search_result(save, meta=meta,head=head) #saves result
            for chunk in df:
                chunk.to_csv(save, mode='a', sep='\t', index=False, header=False) # writes chunks to a new vcf
        else:
            messagebox.showinfo("Oops!", 'You clicked Cancel. Please Try Again')
    except PermissionError: # if output file is opened in another program
        messagebox.showinfo("Error", "Please close the file")
        statusbar['text'] = 'The file is opened in another app'

# Sample entry
sample = StringVar()
entry_sample = Entry(frame, textvariable=sample, width=70)
entry_sample.insert(0, 'Samples')
#entry_sample.bind("<FocusIn>", lambda args: entry_sample.delete('0', 'end'))
entry_sample.grid(row=2, column=0, sticky='news', padx=6, pady=3)

# Sample button
button_sample = Button(frame, text='Extract', bg='#c1c7cf', fg='black', relief='ridge', command=sample_button)
button_sample.grid(row=2, column=1, sticky='news', padx=6, pady=3)

# Function that binds to button, execute conversion function and saves result
@time_it
def sample_file_button():
    path_samples = filedialog.askopenfilename(initialdir="/", title="Select A File With Samples",
                                              filetypes=(("vcf files", "*.txt .vcf"), ("all files", "*.*")))
    samples = sample_file(path_samples)
    save = filedialog.asksaveasfilename(title="Select file", defaultextension='.vcf', filetypes=[("vcf files", ".vcf")])
    sample_search(path, samples, save)
    #
    #total_count=len(samples)
    #statusbar['text'] = '{} samples out of {} input samples in the file were found'.format(count, total_count)


# Extract list of samples from txt with samples
def sample_file(sample_file):
    with open(sample_file, 'r') as f:
        sample_list = [line.strip()for line in f for line in line.split(',')]
    return sample_list

# Sample from txt file button
button_sample_file = Button(frame, text='Extract from File', bg='#c1c7cf', fg='black', relief='ridge',
                                 command=sample_file_button)
button_sample_file.grid(row=2, column=2, sticky='news', padx=6, pady=3)

# Function that binds to button, execute conversion function and saves result
@time_it
def number_gt_to_letter_gt_button():
    letter_gt = number_gt_to_letter_gt(path)
    head = get_header_line(path)
    meta=get_meta(path)
    filename = filedialog.asksaveasfilename(title="Select file", defaultextension='.vcf', filetypes=[("vcf files", ".vcf")])
    save_search_result(filename, letter_gt, meta=meta, head=head)
    statusbar['text'] = 'GT numbers were converted to GT letters'

#GT conversion
def number_gt_to_letter_gt(vcf):
    head = get_header_line(vcf)
    CHROM = head.index('#CHROM')
    for line in open(vcf):
        if '#' in line: #skip lines with '#'
            pass
        elif 'chr' in line: #parse only lines with 'chr'
            arr = line.strip().split('\t')
            arr[CHROM + 8] = 'GT'
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
            output = ra + '\t' + sample_gt + '\n'
            yield output
        else: pass
#
# GT conversion button
button_gt = Button(frame, text='Convert GT', bg='#c1c7cf', fg='black', relief='ridge',
                   command=number_gt_to_letter_gt_button)
button_gt.grid(row=3, column=1, sticky='news', padx=6, pady=3)
button_gt.columnconfigure(0, weight=1)

# Bottom frame
frame_b = Frame(root, bd=1, relief='sunken')
frame_b.grid(row=1, column=0, sticky='we')
frame_b.grid_columnconfigure(0, weight=1)

# Status bar
statusbar = Label(frame_b, text='Welcome to re-Searcher!', bd=3, anchor=W)
credits = Message(frame_b, text='© Laboratory of Bioinformatics and Systems Biology \n Center for Life Sciences, NLA, Nazarbayev University', width=300, bd=3, anchor=E)
statusbar.grid(row=0, column=0, padx=6)
credits.grid(row=0, column=1, padx=6)
##
# APP START
root.mainloop()
