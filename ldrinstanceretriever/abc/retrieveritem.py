
from abc import ABCMeta, abstractmethod


__AUTHOR__ = "Tyler Danstrom"
__EMAIL__ = "tdanstrom@uchicago.edu"
__VERSION__ = "1.0.0"
__DESCRIPTION__ = "a restful application to resolve the various parts of a material suite in the LDR to downloadeable files"
__COPYRIGHT__ = "University of Chicago, 2016"

class RetrieverItem(metaclass=ABCMeta):
    @abstractmethod
    def get_file_data():
        """a method that uses the content_file_path property and the mimetype property to return a
        web response downloadable file of the main content of an LDR material suite.
        """
        pass

    @abstractmethod
    def get_premis_data():
        """a method that uses the premis_file_path property to return a web response downloadable
        file of the main content of an LDR material suite.
        """
        pass

    @abstractmethod
    def find_out_related_objects():
        """a method that uses the premis_core_data property to return a dictionary containing RESTful
        paths to all related objects for a particuar LDR material suite
        """
        pass

    @abstractmethod
    def find_out_technical_metadata():
        """a method that uses the premis_content_file_path to scan the object directory for any metadata records
        that are not PREMIS and are assumed to be technical metadata
        """ 
        pass
