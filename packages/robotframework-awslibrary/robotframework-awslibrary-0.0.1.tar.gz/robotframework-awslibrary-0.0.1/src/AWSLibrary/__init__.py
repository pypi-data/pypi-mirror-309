from .keywords import *
from robotlibcore import DynamicCore


class AWSLibrary(DynamicCore):

    def __init__(self):
        keywords = self.__get_keyword_instances()
        super().__init__(keywords)

    def __get_keyword_instances(self):
        return [s3()]

