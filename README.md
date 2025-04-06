# miniutils
A set of small scripts for simple tasks.

# Image
A set of scripts for manipulating images.

## invert_img.py
Inverts the color of an image.
Usage: `python invert_img.py -p <path_to_image>`

Inverted image will be saved in the same directory with the same name and the suffix '_neg'

# Files
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

# License

This project is distributed under the MIT License. Detailed information is available in the [LICENSE](LICENSE) file.

# Contact

- **Author:** Dmatryus Detry
- **Email:** dmatryus.sqrt49@ysndex.ru

If you have any questions or suggestions for improving the script, please contact me.