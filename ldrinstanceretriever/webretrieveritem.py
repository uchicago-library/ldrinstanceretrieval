from flask import send_file
from ldrpremisbuilding.utils import *
from os import listdir
from os.path import dirname, join

from ldrpremisbuilding.utils import extract_identity_data_from_premis_record
from pypairtree.utils import identifier_to_path

from .abc.retrieveritem import RetrieverItem

__AUTHOR__ = "Tyler Danstrom"
__EMAIL__ = "tdanstrom@uchicago.edu"
__VERSION__ = "1.0.0"
__DESCRIPTION__ = "a restful application to resolve the various parts of a material suite in the LDR to downloadeable files"
__COPYRIGHT__ = "University of Chicago, 2016"

class WebRetrieverItem(RetrieverItem):
    """a class to create an instance of a materialsuite in the resolver application code.

    This class gets instantiated with two parts of an item's identifier: the ark id and
    the object identifier. During instantiation, the class extracts the core information
    from the PREMIS record; evaluates the file extension of for the main content file and
    builds the file paths for the premis record in livePremis and the content and technical
    metadata in longTermStorage
    """
    def __init__(self, arkid, objid, whitelist=True):
        """the initialization method for the AnInstanceItem class

        __Args__
        1. arkid (str): a string nice opaque universal identifier for a particular accession that
                        contains premis record objects
        2. objid (str): a string unique universal identifier for a particular premis record object

        __KWARgs__
        1. whitelist (Boolean):  a flag for whether or not to determine of the content is authorized to be distributed publicly
        """
        self.arkid = arkid
        self.objid = objid

        self.whitelist = "/disk/0/repositoryCode/apistorage/publicurls/whitelist.txt"
        self.content_root = "/data/repository/longTermStorage"
        self.premis_root = "/data/repository/livePremis"
        self.premisid_path = identifier_to_path(objid)
        self.arkid_path = identifier_to_path(arkid)
        self.premis_file_path = join(self.premis_root,
                                     str(identifier_to_path(arkid)),
                                     "arf", "pairtree_root",
                                     str(identifier_to_path(objid)),
                                     "arf", "premis.xml")
        self.content_file_path = join(self.content_root,
                                      str(identifier_to_path(arkid)),
                                      "arf", "pairtree_root",
                                      str(identifier_to_path(objid)),
                                      "arf", "content.file")
        self.premis_core_data = extract_identity_data_from_premis_record(self.premis_file_path)
        self.mimetype = self.premis_core_data.mimetype
        self.extension = self.mimetype.split('/')[1]
        if whitelist:
            if self.get_identifier() in open(self.whitelist, "r").readlines():
                self.public = True
        else:
            self.public = False

    def get_file_data(self):
        """a method that uses the content_file_path property and the mimetype property to return a
        web response downloadable file of the main content of an LDR material suite.
        """
        data = send_file(self.content_file_path, as_attachment=True, attachment_filename=self.objid+self.extension,
                         mimetype=self.mimetype)
        return (self.content_file_path, self.get_identifier().split('/')[1], self.mimetype)

    def get_public_data(self):
        pass

    def get_premis_data(self):
        """a method that uses the premis_file_path property to return a web response downloadable
        file of the main content of an LDR material suite.
        """
        return (self.premis_file_path, self.get_identifier.split('/')[1], "application/xml"))

    def find_out_related_objects(self):
        """a method that uses the premis_core_data property to return a dictionary containing RESTful
        paths to all related objects for a particuar LDR material suite
        """
        output = {}
        tally = 0
        for n_related_object in self.premis_core_data.related_objects:
           output[tally] = {'loc': self.premis_core_data.related_objects[i],
                            'identifier': str(i)}
        return output

    def find_out_technical_metadata(self):
        """a method that returns technical metadata list

        It uses the content_file_path property to check for any metadata in that directory that is
        not PREMIS. Any non-premis metadata in a object directory on-disk can be assumed to be some
        variant of technical metadata. It returns a dictionary containig enumerated sub-dictionaries
        for each technical metadata record discovered with the enumerated name in the key 'label'
        and a RESTFUL path to that particular metadata record in the key 'loc'
        """
        metadata_in_content_directory = [n_record.split('.')[0] for n_record in listdir(dirname(self.content_file_path))
                                         if n_record.endswith('.xml') and 'premis' not in n_record]
        output = {}
        for i in range(len(metadata_in_content_directory)):
            output[str(i)] = {"label": metadata_in_content_directory[i].split('.xml')[0],
                              "loc": self.get_identifier(),
                              "identifier": str(i)}
        return output

    def get_premis_record_object(self):
        return self.premis_core_data.premis_record

    def get_identifier(self):
        return join(self.arkid, self.objid)

    def is_it_public(self):
        return self.public
