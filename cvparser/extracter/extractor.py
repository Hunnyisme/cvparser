from abc import abstractmethod


class Extractor(object):
    """
    extract critical information from Doc object
    """
    def __init__(self, doc):
        self.doc = doc


    @abstractmethod
    def extract(self):
        pass

