# Using CSV module

## DELIMITER:
Default is ',', but you can specify by the option:
```python
csvreader = csv.reader(file, delimiter=':')
```

## HEADERS
Create an empty list called header. Use the next() method to obtain the header.

The .next() method returns the current row and moves to the next row.

The first time you run next() it returns the header and the next time you run it returns the first record and so on.
````python
header = []
header = next(csvreader)
header
````

## PROCESS DATA
Iterate data:
````python
    for row in csvreader:
        print(f"type is: {type(row)} - data: {row}")
````
Row is a List, and contain on its index the data separate by the separator.

## ERRORS

Traceback (most recent call last):  
   File "SCRIPT LOCATION", line NUMBER, in <module>  
     text = file.read()
   File "C:\Python31\lib\encodings\cp1252.py", line 23, in decode  
     return codecs.charmap_decode(input,self.errors,decoding_table)[0]
UnicodeDecodeError: 'charmap' codec can't decode byte 0x90 in position 2907500: character maps to `<undefined>`  


Solution
The file in question is not using the CP1252 encoding. It's using another encoding. Which one you have to figure out yourself. Common ones are Latin-1 and UTF-8. Since 0x90 doesn't actually mean anything in Latin-1, UTF-8 (where 0x90 is a continuation byte) is more likely.

You specify the encoding when you open the file:

file = open(filename, encoding="utf8")


# Using pandas
Steps of reading CSV files using pandas

1. Import pandas library

import pandas as pd
2. Load CSV files to pandas using read_csv()

Basic Syntax: pandas.read_csv(filename, delimiter=’,’)

data= pd.read_csv("Salary_Data.csv")
data