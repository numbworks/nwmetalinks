'''
A library designed to generate MetaLink 4.0 XML files.

Alias: nwml
'''

# GLOBAL MODULES
import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.dom.minidom import Document
from xml.etree.ElementTree import Element, SubElement
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
    def validate_tuple(tpl : tuple[str, str]) -> None:

        '''Validates the URL and filename of the provided tuple.'''

        url, file_name = tpl

        if url is None or not str(url).strip():
            raise Exception(_MessageCollection.provided_file_entry_null_url(tpl))

        if file_name is None or not str(file_name).strip():
            raise Exception(_MessageCollection.provided_file_entry_null_filename(tpl))

    @staticmethod
    def validate_tuples(tuples : list[tuple[str, str]]) -> None:

        '''Validates the provided tuples and their entries.'''

        Validator.validate_instance(instance = tuples, instance_name = "tuples")

        if any(x is None for x in tuples):
            raise ValueError(_MessageCollection.provided_list_contains_null("tuples"))

        for tpl in tuples:
            Validator.validate_tuple(tpl = tpl)

# CLASSES
class MetaLinkFactory():

    '''Collects all the logic related to MetaLink XML generation.'''

    def __map(self, urls : list[str], file_names : list[str]) -> list[tuple[str, str]]:

        '''Maps lists of URLs and filenames into a list of tuples.'''

        tuples : list[tuple[str, str]] = []

        for i in range(len(urls)):
            tuples.append((urls[i], file_names[i]))

        return tuples

    def create_metalink4_from_lists(self, package_name : str, urls : list[str], file_names : list[str]) -> str:

        '''Creates MetaLink 4.0 XML content from separate url and filename lists.'''

        Validator.validate_string(str_val = package_name, str_name = "package_name")
        Validator.validate_urls_and_filenames(urls = urls, file_names = file_names)

        tuples : list[tuple[str, str]] = self.__map(urls = urls, file_names = file_names)
        xml_content : str = self.create_metalink4(package_name = package_name, tuples = tuples)

        return xml_content
    def create_metalink4(self, package_name : str, tuples : list[tuple[str, str]]) -> str:

        '''Creates MetaLink 4.0 XML content from a list of (url, file_name) tuples.'''

        Validator.validate_string(str_val = package_name, str_name = "package_name")
        Validator.validate_tuples(tuples = tuples)

        xml_namespace : str = "urn:ietf:params:xml:ns:metalink"
        ET.register_namespace("", xml_namespace)

        element_metalink : Element = Element(f"{{{xml_namespace}}}metalink", attrib = {"version": "4.0"})

        element_identity : Element = SubElement(element_metalink, f"{{{xml_namespace}}}identity")
        element_identity.text = package_name

        for url, file_name in tuples:
            element_file : Element = SubElement(element_metalink, f"{{{xml_namespace}}}file", attrib = {"name": file_name})
            element_url : Element = SubElement(element_file, f"{{{xml_namespace}}}url")
            element_url.text = url

        xml_raw : bytes = ET.tostring(element_metalink, encoding = "utf-8")
        xml_parsed : Document = minidom.parseString(xml_raw)
        xml_pretty : str = xml_parsed.toprettyxml(indent = "  ", encoding = "utf-8").decode("utf-8")

        return xml_pretty

# MAIN
if __name__ == "__main__":
    pass