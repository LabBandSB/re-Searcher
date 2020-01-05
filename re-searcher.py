from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import time
from datetime import datetime
import re
def time_it(f):
    time_it.active = 0

    def tt(*args, **kwargs):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        time_it.active += 1
        t0 = time.time()
        tabs = '\t'*(time_it.active - 1)
        name = f.__name__
        log_file = open(r"logfile.log", "a")
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
#
# MENU
#
def getting_started():
    os.startfile('Getting started.txt')
def about():
    os.startfile('About.txt')
#
menubar = Menu(root)
root.config(menu=menubar)
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=subMenu)
subMenu.add_command(label='Getting Started', command=getting_started)
subMenu.add_command(label='About', command=about)
#
root.minsize(200, 155)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.title('re-Searcher')
#root.iconbitmap('logo.ico')
#
# background_image = PhotoImage(file ="C:\Users\daniy\Downloads\jupyter_notebooks\g.png")
# background_label = Label(root, image=background_image)
# background_label.place(relwidth=1, relheight=1)
#
# TOP_FRAME
#
frame = Frame(root, bg='#334660', bd=1, relief='sunken')
frame.grid(row=0, column=0, sticky='news')
frame.grid_columnconfigure(0, weight=1)
#
# BROWSE_FILE_FUNC
#
@time_it
def open_file():
    global path
    path = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                      filetypes=(("vcf files", "*.txt .vcf"), ("all files", "*.*")))
    try:
        if path:
            # entry_path.delete(0, END)  # Remove current text in entry
            entry_path.insert(0, path)  # Insert the 'path'
            # print path and open file
            statusbar['text'] = 'The file was found and opened'
        else:
            messagebox.showinfo("Cancel", "Oops! You clicked Cancel")
            statusbar['text'] = 'Oops, find a file again'
    except IOError:
        messagebox.showinfo("Error", "Could not open a file")
#
# BROWSE_FILE_ENTRY
#
entry_path = Entry(frame, width=70)
entry_path.insert(0, 'File directory')
entry_path.bind("<FocusIn>", lambda args: entry_path.delete('0', 'end'))
entry_path.grid(row=0, column=0, sticky='news', padx=6, pady=3)

#
# BROWSE_FILE_BUTTON
button_path = Button(frame, text='Browse', bg='#c1c7cf', fg='black', relief='ridge', command=open_file)
button_path.grid(row=0, column=1, sticky='news', padx=6, pady=3)

#
# HEADER LINE_GET
@time_it
def get_header_line(file):
    for line in open(file):
        if '#CHROM' in line:
            line = line.strip().split('\t')
            return line

def get_meta(file):
    arr=list()
    for line in open(file):
        if '##' in line:
            arr+=[line]
    return arr

#
# EXTRACT_HEADER_ONLY
#
@time_it
def header_save():
    head = get_header_line(path)
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

#
# HEADER_GET_BUTTON
#
button_header = Button(frame, text='Extract Header', bg='#c1c7cf', fg='black', relief='ridge', command=header_save)
button_header.grid(row=0, column=2, sticky='news', padx=6, pady=3)


#
# KEYWORD_BUTTON
#
@time_it
def keyword_button():
    global key, head
    if keyword.get():
        word = [i.strip() for i in keyword.get().split(',')]
        total_count = len(word)
        arr, keyword_list, count = keyword_search(path, word)
        head = get_header_line(path)
        meta=get_meta(path)
        filename = filedialog.asksaveasfilename(title="Select file", defaultextension='.vcf', filetypes=[("vcf files", ".vcf")])
        statusbar['text'] = '{} occurrences of {} keywords in the file were found'.format(count, total_count)
        save_search_result(filename, arr, meta=meta, head=head)
    else:
        messagebox.showinfo("Oops!", "Type a keyword")
#
# KEYWORD SEARCH
#
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
#
# KEYWORD_GET_ENTRY
#
keyword = StringVar()
entry_keyword = Entry(frame, textvariable=keyword, width=70)
entry_keyword.insert(0, 'Keywords')
entry_keyword.bind("<FocusIn>", lambda args: entry_keyword.delete('0', 'end'))
entry_keyword.grid(row=1, column=0, sticky='news', padx=6, pady=3)
#
# KEYWORD_GET_BUTTON
#
button_keyword = Button(frame, text='Extract', bg='#c1c7cf', fg='black', relief='ridge', command=keyword_button)
button_keyword.grid(row=1, column=1, sticky='news', padx=6, pady=3)
#
# MULTIPLE_KEYWORD_FILE_INPUT_FUNCT
#
@time_it
def keyword_file_button():
    path_keywords = filedialog.askopenfilename(initialdir="/", title="Select A File With Keywords",
                                      filetypes=(("vcf files", "*.txt .vcf"), ("all  files", "*.*")))
    head = get_header_line(path)
    meta=get_meta(path)
    arr, keys, count_keywords = keyword_file(path_keywords, path)
    total_count = len(keys)
    filename = filedialog.asksaveasfilename(title="Select file", defaultextension='.vcf', filetypes=[("vcf files", ".vcf")])
    statusbar['text'] = '{} occurrences of {} keywords in the file were found'.format(count_keywords, total_count)
    save_search_result(filename, arr, meta=meta, head=head)

#
#
@time_it
def keyword_file(keyword_file, file):
    with open(keyword_file, 'r') as f:
        keyword_list = [line.strip()for line in f for line in line.split(',')]
        arr, keys, count_keywords = keyword_search(file, keyword_list)
    return arr, keys, count_keywords
#
# MULTIPLE_KEYWORD_FILE_INPUT_BUTTON
#
button_keyword_file = Button(frame, text='Extract from File', bg='#c1c7cf', fg='black', relief='ridge',
                                 command=keyword_file_button)
button_keyword_file.grid(row=1, column=2, sticky='news', padx=6, pady=3)
#
# STATUS_BAR
#
# SAVE
#
@time_it
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
# SAMPLE_BUTTON
#
@time_it
def sample_button():
    if sample.get():
        samples = [i.strip() for i in sample.get().split(',')]
        result_sample, count = sample_search(path, samples)
        unzipped_list = list((zip(*result_sample)))
        filename = filedialog.asksaveasfilename(title="Select file", defaultextension='.vcf', filetypes=[("vcf files", ".vcf")])
        save_list_search_result(filename, unzipped_list)
        #
        total_count = len(samples)
        statusbar['text'] = '{} samples out of {} input samples in the file were found'.format(count, total_count)
    else:
        messagebox.showinfo("Oops!", "Type a sample name")
#
# SAMPLE_SEARCH_FUNC
#
@time_it
def sample_search(vcf, sample_list):
    arr1=list()
    for line in open(vcf):
        if "##" in line:
            pass
        else:
            line = [line.strip().split('\t')]
            arr1 +=line
    zipped_list = list(zip(*arr1))
    arr2 = list()
    count_samples=0
    for column in zipped_list:
        arr2 += [column]
        if 'FORMAT' in column:
            break
    for column in zipped_list:
        for sample in sample_list:
            if sample in column:
                arr2 += [column]
                count_samples+=1
                break
    return arr2, count_samples
#
# SAVE_SAMPLE_RESULT
#
@time_it
def save_list_search_result(file, arr_of_tuples=''):
    meta = get_meta(path)
    new_arr = ['\t'.join(tuple) + '\n' for tuple in arr_of_tuples]
    save_search_result(file, new_arr, meta=meta)
#
# SAMPLE_GET_ENTRY
#
sample = StringVar()
entry_sample = Entry(frame, textvariable=sample, width=70)
entry_sample.insert(0, 'Samples')
entry_sample.bind("<FocusIn>", lambda args: entry_sample.delete('0', 'end'))
entry_sample.grid(row=2, column=0, sticky='news', padx=6, pady=3)
#
# SAMPLE_GET_BUTTON
#
button_sample = Button(frame, text='Extract', bg='#c1c7cf', fg='black', relief='ridge', command=sample_button)
button_sample.grid(row=2, column=1, sticky='news', padx=6, pady=3)
#
# MULTIPLE_SAMPLE_FILE_INPUT_FUNCT
#
@time_it
def sample_file_button():
    path_samples = filedialog.askopenfilename(initialdir="/", title="Select A File With Samples",
                                              filetypes=(("vcf files", "*.txt .vcf"), ("all files", "*.*")))
    samples = sample_file(path_samples)
    result_samples, count = sample_search(path, samples)
    list_of_tuples = list((zip(*result_samples)))
    filename = filedialog.asksaveasfilename(title="Select file", defaultextension='.vcf', filetypes=[("vcf files", ".vcf")])
    save_list_search_result(filename,list_of_tuples)
    #
    total_count=len(samples)
    statusbar['text'] = '{} samples out of {} input samples in the file were found'.format(count, total_count)
#
#
@time_it
def sample_file(sample_file):
    with open(sample_file, 'r') as f:
        sample_list = [line.strip()for line in f for line in line.split(',')]
    return sample_list
#
# MULTIPLE_SAMPLE_FILE_INPUT_BUTTON
#
button_sample_file = Button(frame, text='Extract from File', bg='#c1c7cf', fg='black', relief='ridge',
                                 command=sample_file_button)
button_sample_file.grid(row=2, column=2, sticky='news', padx=6, pady=3)
#
#
@time_it
def number_gt_to_letter_gt_button():
    letter_gt = number_gt_to_letter_gt(path)
    head = get_header_line(path)
    meta=get_meta(path)
    filename = filedialog.asksaveasfilename(title="Select file", defaultextension='.vcf', filetypes=[("vcf files", ".vcf")])
    save_search_result(filename, letter_gt, meta=meta, head=head)
    statusbar['text'] = 'GT numbers were converted to GT letters'

#
@time_it
def number_gt_to_letter_gt(vcf):
    head = get_header_line(vcf)
    CHROM = head.index('#CHROM')
    for line in open(vcf):
        if '#' in line:
            pass
        elif 'chr' in line:
            arr = line.strip().split('\t')
            arr[CHROM + 8] = 'GT'
            ra = '\t'.join(arr[0:CHROM + 9])
            sample_gt = list()
            for gt in arr[CHROM + 9:]:
                gt = gt.split(':')[0]
                if len(arr[CHROM + 3]) > 1 or len(arr[CHROM + 4]) > 1:
                    letter_gt = 'MULTIALLELIC SNP'
                elif gt == '0/0' or gt == '0|0':
                    letter_gt = (arr[CHROM + 3]) * 2
                elif gt == '0/1' or gt == '0|1':
                    letter_gt = (arr[CHROM + 3]) + (arr[CHROM + 4])
                elif gt == '1/1' or gt == '1|1':
                    letter_gt = (arr[CHROM + 4]) * 2
                elif gt == './.':
                    letter_gt = '..'
                sample_gt.append(letter_gt)
            sample_gt = '\t'.join(sample_gt)
            output = ra + '\t' + sample_gt + '\n'
            yield output
        else: pass
#
# GT_CONVERT_BUTTON
button_gt = Button(frame, text='Convert GT', bg='#c1c7cf', fg='black', relief='ridge',
                   command=number_gt_to_letter_gt_button)
button_gt.grid(row=3, column=1, sticky='news', padx=6, pady=3)
button_gt.columnconfigure(0, weight=1)
#
# BOTTOM_FRAME
#
frame_b = Frame(root, bd=1, relief='sunken')
frame_b.grid(row=1, column=0, sticky='we')
frame_b.grid_columnconfigure(0, weight=1)
#
statusbar = Label(frame_b, text='Welcome to re-Searcher!', bd=3, anchor=W)
credits = Label(frame_b, text='(c) LBSB, 2019. All rights reserved', bd=3, anchor=E)
statusbar.grid(row=0, column=0, padx=6)
credits.grid(row=0, column=1, padx=6)
##
# APP START
root.mainloop()
