# miniutils
A set of small scripts for simple tasks.

# Image
A set of scripts for manipulating images.

## invert_img.py
Inverts the color of an image.
Usage: `python invert_img.py -p <path_to_image>`

Inverted image will be saved in the same directory with the same name and the suffix '_neg'

# Files
A collection of utility scripts for file operations and validation.

## file_size_sorter.py
Recursively scans a directory and lists files sorted by their size.

### Usage

#### Command Syntax

```bash
python file_size_sorter.py <directory> [file_count] [--asc]
```

##### Arguments:
- `<directory>`: Path to the directory to scan
- `[file_count]`: Optional. Maximum number of files to display
- `[--asc]`: Optional. Sort from smallest to largest (default is largest to smallest)

#### Usage Examples

1. **Basic usage - show all files sorted by size (largest first):**
   ```bash
   python file_size_sorter.py /path/to/directory
   ```

2. **Show only top 10 largest files:**
   ```bash
   python file_size_sorter.py /path/to/directory 10
   ```

3. **Show files sorted from smallest to largest:**
   ```bash
   python file_size_sorter.py /path/to/directory --asc
   ```

4. **Show 5 smallest files:**
   ```bash
   python file_size_sorter.py /path/to/directory 5 --asc
   ```

### Features

- **Recursive scanning**: Traverses all subdirectories
- **Human-readable sizes**: Displays file sizes in B, KB, MB, GB, TB format
- **Error handling**: Gracefully handles permission errors and inaccessible files
- **Flexible sorting**: Sort by size in ascending or descending order
- **Configurable output**: Limit the number of displayed files
- **Cross-platform**: Works on Windows, macOS, and Linux

### Dependencies

No external dependencies required - uses only Python standard library.

## XML Validator against XSD

This script allows you to check the compliance of an XML file with a specified XSD schema.

### Installation of Dependencies

To run the script, you need the `lxml` library. You can install it using pip:

```bash
pip install lxml
```

### Usage

#### Command Syntax

```bash
python XMLvalidator.py <xml_file> <xsd_file> [options]
```

##### Positional Arguments:
- `<xml_file>`: Path to the XML file you want to validate.
- `<xsd_file>`: Path to the XSD file, which is the schema against which validation will be performed.

##### Optional Arguments:
- `--verbose`, `-v`: Outputs detailed information about validation errors, including line and column numbers.

#### Usage Examples

1. **Simple Validation:**

    ```bash
    python XMLvalidator.py example.xml schema.xsd
    ```

2. **Validation with Detailed Error Information:**

    ```bash
    python XMLvalidator.py example.xml schema.xsd --verbose
    ```

### Example Files

#### Example XML File (`example.xml`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<catalog>
   <book id="bk101">
      <author>Gambardella, Matthew</author>
      <title>XML Developer's Guide</title>
      <genre>Computer</genre>
      <price>44.95</price>
      <publish_date>2000-10-01</publish_date>
      <description>An in-depth look at creating applications with XML.</description>
   </book>
   <book id="bk102">
      <author>Ralls, Kim</author>
      <title>Midnight Rain</title>
      <genre>Fantasy</genre>
      <price>5.95</price>
      <publish_date>2000-12-16</publish_date>
      <description>A former architect battles corporate zombies, an evil sorceress, and her own childhood to become queen of the world.</description>
   </book>
</catalog>
```

#### Example XSD File (`schema.xsd`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
   <xs:element name="catalog">
      <xs:complexType>
         <xs:sequence>
            <xs:element name="book" maxOccurs="unbounded">
               <xs:complexType>
                  <xs:sequence>
                     <xs:element name="author" type="xs:string"/>
                     <xs:element name="title" type="xs:string"/>
                     <xs:element name="genre" type="xs:string"/>
                     <xs:element name="price" type="xs:decimal"/>
                     <xs:element name="publish_date" type="xs:date"/>
                     <xs:element name="description" type="xs:string"/>
                  </xs:sequence>
                  <xs:attribute name="id" type="xs:string" use="required"/>
               </xs:complexType>
            </xs:element>
         </xs:sequence>
      </xs:complexType>
   </xs:element>
</xs:schema>
```

# Project Structure

```
miniutils/
├── files/
│   ├── file_size_sorter.py          # File size sorting utility
│   └── xml/
│       └── validator/
│           ├── XMLvalidator.py      # XML validation against XSD
│           ├── example.xml          # Valid XML example
│           ├── schema.xsd           # XSD schema example
│           └── wrong.xml            # Invalid XML example
├── image/
│   └── invert_img.py                # Image color inversion utility
├── .gitignore
├── LICENSE
└── README.md
```

# License

This project is distributed under the Apache License 2.0. Detailed information is available in the [LICENSE](LICENSE) file.

# Contact

- **Author:** Dmatryus Detry
- **Email:** dmatryus.sqrt49@yandex.ru

If you have any questions or suggestions for improving the scripts, please contact me.