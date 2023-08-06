# JEQDSK
A modern JSON representation of the GEQDSK plasma equilibrium file type.

## About
JEQDSK is a project seeking to encourage the use of the more modern JSON file type in storing data that represents the equilibrium state of a tokamak plasma in a toroidally axisymetric configuration.

The JSON file format is an open standard file format that is language-independent and human readable, with many modern programming languages able to parse it.

## Why should I consider using a JEQDSK over a GEQDSK?
There are many advantages to using the JEQDSK file type over the more longstanding and prevalent GEQDSK.

***JSON files are human readable**. Whilst it is true that someone who is familiar with the GEQDSK file structure can over time become accustomed to identifying which entry and on which line a certain plasma parameter is located at, this is something that a person who is unfamiliar with the GEQDSK will struggle with, requiring them to locate documentation that describes precisely the exact line and position of each piece of data. By moving to a JSON format, anyone can see immediately at first-glance what the data is and where each piece of it is located.

***JSON files are more forgiving**. When working with the GEQDSK file structure one must be careful so as to ensure that the functions used to read and write from/to these files are working as intended. Any small issues can result in the file that is created not being readable on the other end. The scripts used to read/write these files are also not particularly easy to understand. By comparison, the writing/reading to/from a JSON file is performed in a handful of lines in a way that is much clearer for the user to understand what is happening. This makes debugging issues more approachable.

***JSON files can be easily extended**. When working with a GEQDSK file, the user is typically asked to provide a dictionary of data to be written, and is similarly returned a dictionary of data when read. The JEQDSK JSON format works in the same way from a user perspective, such that existing workflows that interface with GEQDSK files would require minimal changes. However, by moving to the JEQDSK format, the user can choose to extend the JEQDSK data structure as they see fit, adding whatever additional entries they see fit. This ease of extension is made possible by the JSON reading/writing utilities - no assumption is made as to the structure of the data itself, hence extending the JEQDSK to additional data types does not require updating said read/write routines. In contrast, the GEQDSK file type is limited to a handful of fields, which may or may not be adequate for the user's use case. So long as the 'standard/core' data is there, an extended JEQDSK can be read by a user who is not expecting to use the additional data that has been added. This is because the user will be working with a dictionary, and will simply not need to interact with any additional data that may or may not be present in an extended JEQDSK.

## Can I convert between the GEQDSK and the JEQDSK?
Yes! The JEQDSK package makes use of the open-source FreeQDSK package for interfacing with GEQDSKs, and includes converters to enable seemless translation between the two formats.

## Installation
TBA

## Usage
A JEQDSK file can be read using the 'jeqdsk.read' function:
```python
from jeqdsk import jeqdsk

data = jeqdsk.read('./data/diiid.jeqdsk')
```
which willl return a dictionary of the data in the JEQDSK.

A JEQDSK can be written using the 'jeqdsk.write' function:
```python
from jeqdsk import jeqdsk

jeqdsk.write('./data/diiid.jeqdsk',data)
```

A JEQDSK can be converted to a new GEQDSK with the 'jeqdsk.convert_jeqdsk_to_geqdsk' function:
```python
from jeqdsk import jeqdsk

jeqdsk.convert_jeqdsk_to_geqdsk('./data/diiid_new.geqdsk','./data/diiid.jeqdsk')
```

A GEQDSK can be converted to a new JEQDSK with the 'jeqdsk.convert_geqdsk_to_jeqdsk' function:
```python
from jeqdsk import jeqdsk

jeqdsk.convert_geqdsk_to_jeqdsk('./data/diiid.geqdsk','./data/diiid_new.jeqdsk')
```

The contents of a JEQDSK can be printed to the console with the 'display_contents' function:
```python
from jeqdsk import jeqdsk

data = jeqdsk.read('./data/diiid.jeqdsk')
jeqdsk.display_contents(data)
```

The contents of a JEQDSK can be visualised graphically with the 'plot_data' function:
```python
from jeqdsk import jeqdsk

data = jeqdsk.read('./data/diiid.jeqdsk')
jeqdsk.plot_data(data)
```

## Contact
Please feel free to contact me through the issues page

## To-do
* Add installation instructions
* Add standard GEQDSK entries description
* PyPi distribution
