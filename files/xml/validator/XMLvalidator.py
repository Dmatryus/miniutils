import argparse

try:
    from lxml import etree
except ImportError:
    print("The lxml library is not installed. Please run pip install lxml")


def validate_xml(xml_file, xsd_file, verbose=False):
    # Parse the XSD file and create an XMLSchema object
    with open(xsd_file, "rb") as f:
        schema_root = etree.XML(f.read())
        schema = etree.XMLSchema(schema_root)
    # Parse the XML file
    with open(xml_file, "rb") as f:
        xml_doc = etree.parse(f)
    # Validate the XML file against the XSD schema
    if schema.validate(xml_doc):
        print("✅  The XML file is valid.")
    else:
        print("❌  The XML file is invalid.")
        for error in schema.error_log:
            if verbose:
                print(
                    f"⚠ Error: {error.message} (Line: {error.line}, Column: {error.column})"
                )
            else:
                print(error.message)


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="XML validator against XSD schema")
    # Add arguments for specifying file paths
    parser.add_argument("xml_file", type=str, help="Path to XML file")
    parser.add_argument("xsd_file", type=str, help="Path to XSD file")
    # Add an optional argument for verbose output
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Output detailed error information"
    )
    # Parse command-line arguments
    args = parser.parse_args()
    # Call the validation function with provided arguments
    validate_xml(args.xml_file, args.xsd_file, verbose=args.verbose)


if __name__ == "__main__":
    main()
