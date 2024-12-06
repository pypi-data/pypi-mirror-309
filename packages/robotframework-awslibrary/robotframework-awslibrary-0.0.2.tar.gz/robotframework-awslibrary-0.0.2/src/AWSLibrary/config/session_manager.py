import boto3
from boto3.session import Session


class SessionManager:
    __instance = None
    __session: Session = boto3.Session()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SessionManager, cls).__new__(cls)
        return cls.__instance

    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, session: Session):
        self.__session = session

