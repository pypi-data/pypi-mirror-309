This is a powerful package for manipulatinf files.
It contains all the attribute and functions in model sky-txt.
So model sky-txt won't be updated from now on.

#Warnings
This packages was called PFI before version 0.0.2.
And now it is called PFL.

#History
-------------------
0.0.1 (2024-11-09}
-------------------
I have written packages since 2022.And I uplowded txt in Feb,2023.
This time I add more files in to this model.

-------------------
0.0.2 (2024-11-16}
-------------------
Fixed a major issue with incompleted packages.

-------------------
0.0.3 (2024-11-16｝
-------------------
Fixed a major issue with syntax errors packages.

# How to use PFL

1. Install PFL
```bash
pip install PythonFileLib
```

2. You're done! Now all there is to do is read the documentation.

# Documentation



1. Load Package
```python
import PFL

dir(PFL)
```

2. get files(examples)
```python
from PFL import file
from file import file
f = file.file('C:/123.py',file.AP)
f.change_extension('.txt')  #it would become 123.txt
f.movefile('D:/')
```

3. Get text in .txt files
```python
from PFL import file
from file import txt

f = txt.txt('C:/123.txt')
f.write("123")
f.write("456")
print(f.read_first_line)  #return 123
f.change_txt_line(2,'123')  #line2 will become 123
```

4. Read .csv files
```python
from PFL import file
from file import csv

f = csv.csv('C:/123.csv')
f.read()
```

# Functions and classes are updating......


