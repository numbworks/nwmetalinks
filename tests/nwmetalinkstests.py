# GLOBAL MODULES
import os
import sys
import unittest

# LOCAL MODULES
sys.path.append(os.path.dirname(__file__).replace('tests', 'src'))
from nwmetalinks import _MessageCollection, Validator, MetaLinkFactory

# SUPPORT METHODS
# TEST CLASSES
class ValidatorTestCase(unittest.TestCase):

    def test_validatestring_shouldraisevalueerror_whenstringisnone(self) -> None:

        # Arrange
        str_val : str = None # type: ignore
        str_name : str = "package_name"
        expected : str = _MessageCollection.provided_package_name_null_or_empty(str_name)

        # Act, Assert
        with self.assertRaises(ValueError) as context:
            Validator.validate_string(str_val = str_val, str_name = str_name)

        self.assertEqual(expected, str(context.exception))
    def test_validatestring_shouldraisevalueerror_whenstringiswhitespace(self) -> None:

        # Arrange
        str_val : str = "   "
        str_name : str = "package_name"
        expected : str = _MessageCollection.provided_package_name_null_or_empty(str_name)

        # Act, Assert
        with self.assertRaises(ValueError) as context:
            Validator.validate_string(str_val = str_val, str_name = str_name)

        self.assertEqual(expected, str(context.exception))
    def test_validatestring_shoulddonothing_whenstringisvalid(self) -> None:

        # Arrange
        str_val : str = "package"

        # Act, Assert
        Validator.validate_string(str_val = str_val)

    def test_validateinstance_shouldraisevalueerror_wheninstanceisnone(self) -> None:

        # Arrange
        instance : object = None
        instance_name : str = "files"
        expected : str = _MessageCollection.provided_instance_null(instance_name)

        # Act, Assert
        with self.assertRaises(ValueError) as context:
            Validator.validate_instance(instance = instance, instance_name = instance_name)

        self.assertEqual(expected, str(context.exception))
    def test_validateinstance_shoulddonothing_wheninstanceisvalid(self) -> None:

        # Arrange
        instance : object = []

        # Act, Assert
        Validator.validate_instance(instance = instance)

    def test_validatelist_shouldraisevalueerror_whenlistcontainsnone(self) -> None:

        # Arrange
        lst : list = [1, None, 3]
        lst_name : str = "urls"
        expected : str = _MessageCollection.provided_list_contains_null(lst_name)

        # Act, Assert
        with self.assertRaises(ValueError) as context:
            Validator.validate_list(lst = lst, lst_name = lst_name)

        self.assertEqual(expected, str(context.exception))

    def test_validateurlsandfilenames_shouldraisevalueerror_whencountsdonotmatch(self) -> None:

        # Arrange
        urls : list[str] = ["https://example.com/file1.zip"]
        file_names : list[str] = ["file1.zip", "file2.zip"]
        expected : str = _MessageCollection.list_counts_do_not_match()

        # Act, Assert
        with self.assertRaises(ValueError) as context:
            Validator.validate_urls_and_filenames(urls = urls, file_names = file_names)

        self.assertEqual(expected, str(context.exception))

    def test_validatefile_shouldraiseexception_whenurlisnone(self) -> None:

        # Arrange
        file_tuple : tuple[str, str] = (None, "file.zip") # type: ignore
        expected : str = _MessageCollection.provided_file_entry_null_url(file_tuple)

        # Act, Assert
        with self.assertRaises(Exception) as context:
            Validator.validate_tuple(tpl = file_tuple)

        self.assertEqual(expected, str(context.exception))
    def test_validatefile_shouldraiseexception_whenfilenameiswhitespace(self) -> None:

        # Arrange
        file_tuple : tuple[str, str] = ("https://example.com/file.zip", "  ")
        expected : str = _MessageCollection.provided_file_entry_null_filename(file_tuple)

        # Act, Assert
        with self.assertRaises(Exception) as context:
            Validator.validate_tuple(tpl = file_tuple)

        self.assertEqual(expected, str(context.exception))
class MetaLinkFactoryTestCase(unittest.TestCase):

    def test_map_shouldreturnexpectedtuples_wheninvoked(self) -> None:

        # Arrange
        urls : list[str] = [
            "https://numbworks.github.io/NW.MetaLinks.zip", 
            "https://numbworks.github.io/NW.MetaLinks.tar.gz"
        ]
        file_names : list[str] = [
            "NW.MetaLinks.zip", 
            "NW.MetaLinks.tar.gz"
        ]
        expected : list[tuple[str, str]] = [
            ("https://numbworks.github.io/NW.MetaLinks.zip", "NW.MetaLinks.zip"),
            ("https://numbworks.github.io/NW.MetaLinks.tar.gz", "NW.MetaLinks.tar.gz")
        ]

        # Act
        actual : list[tuple[str, str]] = MetaLinkFactory()._MetaLinkFactory__map(urls = urls, file_names = file_names) # type: ignore

        # Assert
        self.assertEqual(expected, actual)

    def test_createmetalink4fromlists_shouldraisevalueerror_whenpackagenameisnone(self) -> None:

        # Arrange
        package_name : str = None # type: ignore
        urls : list[str] = ["https://numbworks.github.io/NW.MetaLinks.zip"]
        file_names : list[str] = ["NW.MetaLinks.zip"]

        # Act, Assert
        with self.assertRaises(ValueError) as context:
            MetaLinkFactory().create_metalink4_from_lists(package_name = package_name, urls = urls, file_names = file_names)

        self.assertIn("cannot be None", str(context.exception))
    def test_createmetalink4fromlists_shouldreturnexpectedmetalink_whenproperurlsandfilenames(self) -> None:

        # Arrange
        package_name : str = "NW.MetaLinks"
        urls : list[str] = [
            "https://numbworks.github.io/NW.MetaLinks.zip",
            "https://numbworks.github.io/NW.MetaLinks.tar.gz"
        ]
        file_names : list[str] = [
            "NW.MetaLinks.zip",
            "NW.MetaLinks.tar.gz"
        ]

        expected : str = (
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<metalink xmlns="urn:ietf:params:xml:ns:metalink" version="4.0">\n'
            '  <identity>NW.MetaLinks</identity>\n'
            '  <file name="NW.MetaLinks.zip">\n'
            '    <url>https://numbworks.github.io/NW.MetaLinks.zip</url>\n'
            '  </file>\n'
            '  <file name="NW.MetaLinks.tar.gz">\n'
            '    <url>https://numbworks.github.io/NW.MetaLinks.tar.gz</url>\n'
            '  </file>\n'
            '</metalink>\n'
        )

        # Act
        actual : str = MetaLinkFactory().create_metalink4_from_lists(package_name = package_name, urls = urls, file_names = file_names)

        # Assert
        self.assertEqual(expected, actual)

    def test_createmetalink4_shouldreturnexpectedmetalink_whenpropertuples(self) -> None:

        # Arrange
        package_name : str = "NW.MetaLinks"
        tuples : list[tuple[str, str]] = [
            ("https://numbworks.github.io/NW.MetaLinks.zip", "NW.MetaLinks.zip"),
            ("https://numbworks.github.io/NW.MetaLinks.tar.gz", "NW.MetaLinks.tar.gz")
        ]

        expected : str = (
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<metalink xmlns="urn:ietf:params:xml:ns:metalink" version="4.0">\n'
            '  <identity>NW.MetaLinks</identity>\n'
            '  <file name="NW.MetaLinks.zip">\n'
            '    <url>https://numbworks.github.io/NW.MetaLinks.zip</url>\n'
            '  </file>\n'
            '  <file name="NW.MetaLinks.tar.gz">\n'
            '    <url>https://numbworks.github.io/NW.MetaLinks.tar.gz</url>\n'
            '  </file>\n'
            '</metalink>\n'
        )

        # Act
        actual : str = MetaLinkFactory().create_metalink4(package_name = package_name, tuples = tuples)

        # Assert
        self.assertEqual(expected, actual)
    def test_createmetalink4_shouldreturnexpectedmetalink_whenargumentscontainxmlcharacters(self) -> None:

        # Arrange
        package_name : str = "NW.MetaLinks & Tests"
        files : list[tuple[str, str]] = [
            ("https://numbworks.github.io/package.zip?version=1&platform=windows", 'package & "tests".zip')
        ]

        expected : str = (
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<metalink xmlns="urn:ietf:params:xml:ns:metalink" version="4.0">\n'
            '  <identity>NW.MetaLinks &amp; Tests</identity>\n'
            '  <file name="package &amp; &quot;tests&quot;.zip">\n'
            '    <url>https://numbworks.github.io/package.zip?version=1&amp;platform=windows</url>\n'
            '  </file>\n'
            '</metalink>\n'
        )

        # Act
        actual : str = MetaLinkFactory().create_metalink4(package_name = package_name, tuples = files)

        # Assert
        self.assertEqual(expected, actual)

# MAIN
if __name__ == "__main__":
    result = unittest.main(argv=[''], verbosity=3, exit=False)