'''
A library designed to generate MetaLink 4.0 XML files.

Alias: nwml
'''

# GLOBAL MODULES
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Optional

# LOCAL MODULES
# CONSTANTS
# STATIC CLASSES
class _MessageCollectionValidator():

    '''Collects all the messages used for logging and for the exceptions used by Validator.'''

    @staticmethod
    def provided_package_name_null_or_empty(package_name_name : str = "package_name") -> str:
        return f"'{package_name_name}' cannot be None, empty, or whitespace."

    @staticmethod
    def provided_instance_null(instance_name : str) -> str:
        return f"'{instance_name}' cannot be None."

    @staticmethod
    def provided_list_contains_null(lst_name : str) -> str:
        return f"'{lst_name}' contains one or more null entries."

    @staticmethod
    def list_counts_do_not_match(urls_name : str = "urls", file_names_name : str = "file_names") -> str:
        return f"'{urls_name}' and '{file_names_name}' must have the same number of items."

    @staticmethod
    def provided_file_entry_null_url(file_entry : tuple) -> str:
        return f"The provided file entries has a null or empty url ('{file_entry}')."

    @staticmethod
    def provided_file_entry_null_filename(file_entry : tuple) -> str:
        return f"The provided file entries has a null or empty fileName ('{file_entry}')."
class _MessageCollection(
        _MessageCollectionValidator):

    '''Collects all the messages used for logging and for the exceptions.'''
class Validator():

    '''Collects all validation methods.'''

    @staticmethod
    def validate_string(str_val : Optional[str], str_name : str = "str") -> None:

        '''Validates that the provided string is not None, empty, or whitespace.'''

        if str_val is None or not str(str_val).strip():
            raise ValueError(_MessageCollection.provided_package_name_null_or_empty(str_name))

    @staticmethod
    def validate_instance(instance : object, instance_name : str = "instance") -> None:

        '''Validates that the provided instance is not None.'''

        if instance is None:
            raise ValueError(_MessageCollection.provided_instance_null(instance_name))

    @staticmethod
    def validate_list(lst : list, lst_name : str = "lst") -> None:

        '''Validates the provided list and its entries.'''

        Validator.validate_instance(instance = lst, instance_name = lst_name)

        if any(x is None for x in lst):
            raise ValueError(_MessageCollection.provided_list_contains_null(lst_name))

    @staticmethod
    def validate_urls_and_filenames(urls : list[str], file_names : list[str]) -> None:

        '''Validates the provided urls and their corresponding file_names.'''

        Validator.validate_list(lst = urls, lst_name = "urls")
        Validator.validate_list(lst = file_names, lst_name = "file_names")

        if len(urls) != len(file_names):
            raise ValueError(_MessageCollection.list_counts_do_not_match(urls_name = "urls", file_names_name = "file_names"))

    @staticmethod
    def validate_file(file_tuple : tuple[str, str]) -> None:

        '''Validates the URL and filename of the provided file tuple.'''

        url, file_name = file_tuple

        if url is None or not str(url).strip():
            raise Exception(_MessageCollection.provided_file_entry_null_url(file_tuple))

        if file_name is None or not str(file_name).strip():
            raise Exception(_MessageCollection.provided_file_entry_null_filename(file_tuple))

    @staticmethod
    def validate_files(files : list[tuple[str, str]]) -> None:

        '''Validates the provided files and their entries.'''

        Validator.validate_instance(instance = files, instance_name = "files")

        if any(x is None for x in files):
            raise ValueError(_MessageCollection.provided_list_contains_null("files"))

        for file_tuple in files:
            Validator.validate_file(file_tuple = file_tuple)

# CLASSES
class MetaLinkFactory():

    '''Collects all the logic related to MetaLink XML generation.'''

    def __map(self, urls : list[str], file_names : list[str]) -> list[tuple[str, str]]:

        '''Maps lists of URLs and filenames into a list of tuples.'''

        files : list[tuple[str, str]] = []

        for i in range(len(urls)):
            files.append((urls[i], file_names[i]))

        return files

    def create_metalink4_from_lists(self, package_name : str, urls : list[str], file_names : list[str]) -> str:

        '''Creates MetaLink 4.0 XML content from separate url and filename lists.'''

        Validator.validate_string(str_val = package_name, str_name = "package_name")
        Validator.validate_urls_and_filenames(urls = urls, file_names = file_names)

        files : list[tuple[str, str]] = self.__map(urls = urls, file_names = file_names)

        return self.create_metalink4(package_name = package_name, files = files)
    def create_metalink4(self, package_name : str, files : list[tuple[str, str]]) -> str:

        '''Creates MetaLink 4.0 XML content from a list of (url, file_name) tuples.'''

        Validator.validate_string(str_val = package_name, str_name = "package_name")
        Validator.validate_files(files = files)

        xml_namespace : str = "urn:ietf:params:xml:ns:metalink"
        ET.register_namespace("", xml_namespace)

        metalink_elem : ET.Element = ET.Element(f"{{{xml_namespace}}}metalink", attrib = {"version": "4.0"})

        identity_elem : ET.Element = ET.SubElement(metalink_elem, f"{{{xml_namespace}}}identity")
        identity_elem.text = package_name

        for url, file_name in files:
            file_elem : ET.Element = ET.SubElement(metalink_elem, f"{{{xml_namespace}}}file", attrib = {"name": file_name})
            url_elem : ET.Element = ET.SubElement(file_elem, f"{{{xml_namespace}}}url")
            url_elem.text = url

        raw_xml : bytes = ET.tostring(metalink_elem, encoding = "utf-8")
        parsed : minidom.Document = minidom.parseString(raw_xml)
        pretty_xml : str = parsed.toprettyxml(indent = "  ", encoding = "utf-8").decode("utf-8")

        return pretty_xml

# MAIN
if __name__ == "__main__":
    pass