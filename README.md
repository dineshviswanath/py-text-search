# Py Text Search 🔍

## Install
```bash
virtualenv env_py_final -p python3
. ./env_py_final/bin/activate
pip install -r requirements.txt
```

## Usage
```bash
python cli.py data
```

Sample output
```bash
python cli.py data
2 files read in the directory
Search> to be romeo or not
romeo_juliet.txt | 100.00% match | 1440 occurrences
file1.txt | 80.00% match | 7 occurrences
Search> mars
no matches found
Search> :quit
bye!

```


## Test and Flake8
```bash
tox
```

## Implementation Details
+ What constitutes a word? Punctuations are removed to process the words. 
```
Hello! and Hello are same
```
+ What constitutes two words being equal (and matching) ? case-insensity is implemented.
```
The and the are same
```
+ Data structure design: the in memory representation to search against
```
dictionary[fileName]: dictinary[word]:count
```
+ Ranking design
In addition to number of words match; sum of occurrences of those words are used in ranking to improve results
```
Search> romeo to be or not
romeo_juliet.txt | 100.00% match | 1440 occurrences
file1.txt | 80.00% match | 7 occurrences
```
+ Performance on Huge files
Python generator used to overcome memory issues when reading huge files. Current code is tested with 10GB file.
We can improve usability of the tool by showing progress bar when loading the file.

## Further Enhancements
+ Add click(Command Line Interface Creation Kit) integration
+ Creating/showing progress when reading huge file
+ Docker
