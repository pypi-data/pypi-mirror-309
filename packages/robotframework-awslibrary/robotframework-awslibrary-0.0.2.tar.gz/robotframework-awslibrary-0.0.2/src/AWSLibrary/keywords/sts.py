import boto3
from robot.api.deco import keyword
from AWSLibrary.config.session_manager import SessionManager


class STS:

    def __init__(self) -> None:
        self.session_manager = SessionManager()

    @keyword('STS Assume Role')    
    def assume_role(self, role_arn: str, session_name: str = 'RobotFrameworkSession'):
        sts_client = self.session_manager.session.client('sts')

        response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=session_name
        )

        credentials = response['Credentials']

        assumed_session = boto3.Session(
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

        self.session_manager.session = assumed_session

        return assumed_session

    @keyword('STS Get Caller Identity')
    def get_caller_identity(self):
        sts_client = self.session_manager.session.client('sts')

        response = sts_client.get_caller_identity()

        return response