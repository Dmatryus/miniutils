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

## Universal Markdown Converter

A powerful Markdown to HTML/PDF converter with advanced features including Mermaid diagram support, syntax highlighting, and multiple themes.

### Features

- **Multiple output formats**: HTML and PDF generation
- **Mermaid diagrams**: Render diagrams both locally and via online services
- **Syntax highlighting**: Code blocks with customizable styles (Pygments)
- **Multiple themes**: Default, Dark, GitHub, and Minimal themes
- **Image embedding**: Embed images as base64 in output files
- **HTML minification**: Optimize output file size
- **Table of contents**: Auto-generate TOC from headers
- **Standalone documents**: Create self-contained HTML/PDF files

### Installation

#### Basic dependencies

```bash
pip install markdown beautifulsoup4 requests pygments
```

#### For PDF generation (optional)

```bash
pip install playwright
playwright install chromium
```

### Usage

#### Command Syntax

```bash
python files/md/md_converter.py <input.md> [options]
```

##### Options:
- `--format FORMAT`: Output format: `html` (default) or `pdf`
- `--output FILE`: Output filename (auto-generated if not specified)
- `--theme THEME`: Document theme: `default`, `dark`, `github`, `minimal`
- `--style STYLE`: Code highlighting style (default: `monokai`)
- `--online`: Use online service for Mermaid rendering (no Chromium required)
- `--minify`: Minify HTML output
- `--no-standalone`: Generate only HTML body (no complete document)
- `--no-embed`: Don't embed images in HTML
- `--toc`: Add table of contents
- `--list-styles`: Show all available syntax highlighting styles

#### Usage Examples

1. **Basic HTML conversion:**
   ```bash
   python files/md/md_converter.py document.md
   ```

2. **Generate PDF with dark theme:**
   ```bash
   python files/md/md_converter.py document.md --format pdf --theme dark
   ```

3. **HTML with GitHub styling:**
   ```bash
   python files/md/md_converter.py document.md --style github --theme github
   ```

4. **Use online Mermaid rendering (no Chromium needed):**
   ```bash
   python files/md/md_converter.py document.md --format pdf --online
   ```

5. **Minified HTML with table of contents:**
   ```bash
   python files/md/md_converter.py document.md --minify --toc
   ```

6. **Custom output filename:**
   ```bash
   python files/md/md_converter.py document.md --output report.pdf --format pdf
   ```

7. **List available code highlighting styles:**
   ```bash
   python files/md/md_converter.py --list-styles
   ```

### Supported Markdown Extensions

- Tables
- Fenced code blocks
- Footnotes
- Definition lists
- Abbreviations
- Attributes
- Mermaid diagrams

### Example Markdown with Mermaid

```markdown
# My Document

## Architecture Diagram

\```mermaid
graph TD
    A[Client] --> B[Server]
    B --> C[Database]
\```

## Code Example

\```python
def hello_world():
    print("Hello, World!")
\```
```

### Available Themes

1. **Default**: Clean, professional look with blue accents
2. **Dark**: Dark background with light text
3. **GitHub**: GitHub-style markdown rendering
4. **Minimal**: Simple, typography-focused design

### Popular Code Highlighting Styles

- `monokai` - Dark theme with vibrant colors
- `dracula` - Popular dark theme
- `github` - Light theme in GitHub style
- `vs` - Visual Studio light theme
- `solarized-dark` - Solarized dark color scheme
- `solarized-light` - Solarized light color scheme

Use `--list-styles` to see all available styles (50+ options).

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
python files/xml/validator/XMLvalidator.py <xml_file> <xsd_file> [options]
```

##### Positional Arguments:
- `<xml_file>`: Path to the XML file you want to validate.
- `<xsd_file>`: Path to the XSD file, which is the schema against which validation will be performed.

##### Optional Arguments:
- `--verbose`, `-v`: Outputs detailed information about validation errors, including line and column numbers.

#### Usage Examples

1. **Simple Validation:**

    ```bash
    python files/xml/validator/XMLvalidator.py example.xml schema.xsd
    ```

2. **Validation with Detailed Error Information:**

    ```bash
    python files/xml/validator/XMLvalidator.py example.xml schema.xsd --verbose
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
│   ├── md/
│   │   └── md_converter.py          # Universal Markdown to HTML/PDF converter
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

# Requirements

## Python Version
- Python 3.6 or higher

## Dependencies by Module

| Module | Required Dependencies | Optional Dependencies |
|--------|--------------------|---------------------|
| `invert_img.py` | `Pillow` | - |
| `file_size_sorter.py` | - | - |
| `md_converter.py` | `markdown`, `beautifulsoup4` | `playwright`, `pygments`, `requests` |
| `XMLvalidator.py` | `lxml` | - |

## Quick Install All Dependencies

```bash
# Install all required dependencies
pip install pillow lxml markdown beautifulsoup4 pygments requests

# For full PDF support (optional)
pip install playwright
playwright install chromium
```

# License

This project is distributed under the Apache License 2.0. Detailed information is available in the [LICENSE](LICENSE) file.

# Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

# Contact

- **Author:** Dmatryus Detry
- **Email:** dmatryus.sqrt49@yandex.ru

If you have any questions or suggestions for improving the scripts, please contact me.