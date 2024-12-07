
import importlib.metadata 
import logging
nmrstar_xml_logger = logging.getLogger(__name__)
from nmrstar_xml.translate import Translator

__version__ =  importlib.metadata.version('nmrstar_xml') 

