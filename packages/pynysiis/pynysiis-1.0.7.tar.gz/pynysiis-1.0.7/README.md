## pynysiis

The `nysiis` package provides a Python implementation of the [New York State Identification and Intelligence System](https://en.wikipedia.org/wiki/New_York_State_Identification_and_Intelligence_System) (NYSIIS) phonetic encoding algorithm. NYSIIS encodes names based on pronunciation, which is helpful in name-matching and searching applications.

### Requirements

Python 3.8 and later.

### Setup

You can install this package by using the pip tool and installing:

```python
pip install pynysiis
## OR
easy_install pynysiis
```

Install from source with:

```python
python setup.py install --user

## or `sudo python setup.py install` to install the package for all users
```

### Basic Usage

```python
from nysiis import NYSIIS

encoder = NYSIIS()
name = "Watkins"
encoded_name = encoder.encode(name)
print(encoded_name)  # Output: WATCAN
```

### Name Comparison

```python
from nysiis import NYSIIS

encoder = NYSIIS()

# Compare similar names
name1 = "John Smith"
name2 = "John Smyth"

encoded_name1 = encoder.encode(name1)
encoded_name2 = encoder.encode(name2)

if encoded_name1 == encoded_name2:
    print("Names match phonetically")
else:
    print("Names are phonetically different")

# Output: Names match phonetically
```

### Multi-Language Support

The NYSIIS encoder handles names from various languages:

```python
from nysiis import NYSIIS

encoder = NYSIIS()

# Sample names from different languages
names = [
    # English names
    "Watkins",
    "Robert Johnson",
    
    # Yoruba name
    "Olanrewaju Akinyele",
    
    # Igbo name
    "Obinwanne Obiora",
    
    # Hausa name
    "Abdussalamu Abubakar",
    
    # Hindi name
    "Virat Kohli",
    
    # Urdu name
    "Usman Shah"
]

# Process each name
for name in names:
    encoded_name = encoder.encode(name)
    print(f"{name:<20} -> {encoded_name}")

# Output:
# Watkins              -> WATCAN
# Robert Johnson       -> RABART
# Olanrewaju Akinyele -> OLANRA
# Obinwanne Obiora    -> OBAWAN
# Abdussalamu Abubakar-> ABDASA
# Virat Kohli         -> VARATC
# Usman Shah          -> USNANS
```

### Common Use Cases

#### Database Search Optimisation

```python
def find_similar_names(search_name, database_names):
    encoder = NYSIIS()
    search_code = encoder.encode(search_name)
    
    matches = [
        name for name in database_names
        if encoder.encode(name) == search_code
    ]
    return matches
```

#### Name Deduplication

```python
def find_duplicates(names):
    encoder = NYSIIS()
    encoded_names = {}
    
    for name in names:
        code = encoder.encode(name)
        encoded_names.setdefault(code, []).append(name)
        
    return {
        code: names 
        for code, names in encoded_names.items() 
        if len(names) > 1
    }
```

#### Fuzzy Name Matching

```python
def match_names(name1, name2, encoder=None):
    if encoder is None:
        encoder = NYSIIS()
        
    return encoder.encode(name1) == encoder.encode(name2)
```

### Best Practices

#### Reuse the Encoder Instance

```python
# Good - create once, use many times
encoder = NYSIIS()
for name in large_name_list:
    encoded = encoder.encode(name)

# Less efficient - creating new instance repeatedly
for name in large_name_list:
    encoded = NYSIIS().encode(name)
```

#### Handle Empty Inputs

```python
def process_name(name):
    if not name or not name.strip():
        return None
    
    encoder = NYSIIS()
    return encoder.encode(name)
```

#### Case Sensitivity

```python
# The encoder handles case automatically
encoder = NYSIIS()
print(encoder.encode("smith"))  # Same as "SMITH"
print(encoder.encode("SMITH"))  # Same result
```

### Reference

```tex
@inproceedings{Rajkovic2007,
  author    = {Petar Rajkovic and Dragan Jankovic},
  title     = {Adaptation and Application of Daitch-Mokotoff Soundex Algorithm on Serbian Names},
  booktitle = {XVII Conference on Applied Mathematics},
  editors   = {D. Herceg and H. Zarin},
  pages     = {193--204},
  year      = {2007},
  publisher = {Department of Mathematics and Informatics, Novi Sad},
  url       = {https://jmp.sh/hukNujCG}
}
```

### Additional References

+ [Commission Implementing Regulation (EU) 2016/480](https://www.legislation.gov.uk/eur/2016/480/contents)
+ [Commission Implementing Regulation (EU) 2023/2381](https://eur-lex.europa.eu/eli/reg_impl/2023/2381/oj)

### License

This project is licensed under the [MIT License](./LICENSE).

### Copyright

(c) 2024 [Finbarrs Oketunji](https://finbarrs.eu/). All Rights Reserved.