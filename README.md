# re-Searcher


![logo](https://user-images.githubusercontent.com/56155720/66301515-18245800-e919-11e9-9f90-297352306c9f.png)

re-Searcher is a toolbox aimed to simplify the task for genomics data mining from VCF files. Now there's no need to perform difficult script manipulations in IDE with Python or R. re-Searcher can work with any variant of VCF, for instance, with annotated VCF in ANNOVAR.

## 🚀 Quick Start
1. Click on **Releases** on the right side of this page and download re-Searcher.zip from the latest release.
2. Unzip the archive file with WinRAR or 7zip.
3. Execute **re-searcher** file to run the tool.

## ✅  Features
1.	Browse and open VCF files.

2.	Extract header from VCF to new VCF.

3.	Extract lines containing user input keywords from the input entry or from a Text Document (.txt) file to new VCF file. 
e.g. if you want filter your VCF file to only have rows with 'INDEL' keyword in them. 

4.	Extract columns with user input samples from the input entry or from a Text Document (.txt) file to a new VCF file.  Unnecessary samples from original VCF will be cut off and only user input samples will be remained. 
e.g. if you want filter your VCF file to only have two samples: WE0001 and WE006.

5.	Convert genotype (GT) format from number GT to letter GT. 
Original GT format is numeric (0/0, 0/1, 1/0 or 1/1, etc.), whereas 0 is reference (REF) allele and 1 is alternative (ALT) allele. Multiallelic rows (0/3, 3/2) will be converted by inserting respective ALT allele.

<img src="https://user-images.githubusercontent.com/56155720/66289928-c3c0ae80-e8ff-11e9-9dc2-5008d49ba5f5.png" width="500"/>

<img src="https://user-images.githubusercontent.com/56155720/66289919-c1f6eb00-e8ff-11e9-8909-977f9f9e4371.png" width="500"/>

## ⚒   Usage
●	To open VCF file, click ‘Browse’ button and find your file's location:

<img src="https://user-images.githubusercontent.com/56155720/66289437-87408300-e8fe-11e9-8d0d-d1fd4f1d4ccf.png" width="500"/>

●	To extract header from VCF, click ‘Extract Header’ button:

<img src="https://user-images.githubusercontent.com/56155720/66289920-c28f8180-e8ff-11e9-8978-bfb95522538f.png" width="500"/>

Program will ask you where to save an output file with extracted Header. 

●	To search and extract lines with certain user input keywords, firstly, input your keywords in ‘Keywords’ entry, and then press ‘Extract’ button.

<img src="https://user-images.githubusercontent.com/56155720/66289921-c28f8180-e8ff-11e9-9c9e-5f1de8b3494d.png" width="500"/>

●	 In cases when there are too many keywords, it is inconvenient to input them manually. Create Text Document and copy all necessary keywords in one column.

<img src="https://user-images.githubusercontent.com/56155720/66290103-2fa31700-e900-11e9-8cc9-6dd730019dbe.png" width="300"/>

Then, press ‘Extract from File’ button, after which program ask you to open the Text Document with keywords that you had created.

<img src="https://user-images.githubusercontent.com/56155720/66289922-c28f8180-e8ff-11e9-889a-ddc1e2a63b97.png" width="500"/>

●	To search and extract user input samples (columns), firstly, input your keywords in ‘Sample’ entry, and then press ‘Extract’ button. Program will cut off unnecessary samples.

<img src="https://user-images.githubusercontent.com/56155720/66289923-c28f8180-e8ff-11e9-836e-6d9b90a2759d.png" width="500"/>

●	 Similarly as multiple keywords search from a file, you can input a file with samples. Create .txt and copy all necessary samples in one column.

<img src="https://user-images.githubusercontent.com/56155720/66290100-2fa31700-e900-11e9-90b5-8f6d036ee22e.png" width="300"/>

Then, press ‘Extract from File’ button, after which program ask you to open the .txt with keywords that you had created.

<img src="https://user-images.githubusercontent.com/56155720/66289925-c3281800-e8ff-11e9-850d-fc5974b960cf.png" width="500"/>

●	To convert the numeric GT format to letter GT format press ‘Convert GT’ button.

<img src="https://user-images.githubusercontent.com/56155720/66289927-c3281800-e8ff-11e9-9da4-b87957d76775.png" width="500"/>

## 🤝 Contributing
●Contributions, issues and feature requests are welcome.
Feel free to check [issues page](https://github.com/LabBandSB/re-Searcher/issues) if you want to contribute.


## Credits
●	re-Searcher was created in Laboratory of Bioinformatics and  Systems Biology, Center for Life Sciences, National Laboratory Astana-Nazarbayev University

## 📝 License
●	Copyright 2019 © LBSB.

