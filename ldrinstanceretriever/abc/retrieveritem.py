
from abc import ABCMeta, abstractmethod

class Retriever(metaclass=ABCMeta):
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
        pass
