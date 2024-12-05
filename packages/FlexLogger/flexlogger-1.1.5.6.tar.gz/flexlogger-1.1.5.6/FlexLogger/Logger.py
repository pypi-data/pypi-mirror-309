import socket

import requests

from FlexLogger.Log import Classification, SyslogLevel


class Logger:
    """
    A class for logging messages and sending them to a specified endpoint server with customizable details such as
    application, classification, source, and system log level. The Logger class can track errors based on log
    severity levels and handle different types of log submissions.

    Attributes:
        application (str): The name of the application generating the logs.
        __api_url (str): The complete URL for the endpoint server.
        __token (str): The authorization token for API requests.
        __source (str): Indicates whether the source is "Local", "Remote" or the IP from the sender, if possible.
        __hadError (bool): Flag indicating whether any error-level messages have been logged.
    """

    def __init__(self, endpoint_server: str, endpoint_port: int, endpoint_command: str, api_token: str, application: str, resolveRemoteSource: bool = False):
        """
        Initializes a Logger instance with specified endpoint and authorization details.

        Args:
            endpoint_server (str): The server to which logs will be sent.
            endpoint_port (int): The port on the endpoint server.
            endpoint_command (str): The specific command or path on the endpoint.
            api_token (str): The API token for authenticating log submissions.
            application (str): The application name associated with the logs.
        """
        self.application = application

        # API and Token prepare
        self.__api_url = f"https://{endpoint_server}:{endpoint_port}/{endpoint_command}"
        self.__token = api_token

        # Host detection

        if socket.gethostname() == endpoint_server:
            self.__source = "Local"
        else:
            if resolveRemoteSource:
                try:
                    self.__source = requests.get("https://api.ipify.org").text
                except requests.RequestException:
                    self.__source = "Remote"
            else:
                self.__source = "Remote"

        # Error Mark
        self.__hadError = False

    def smartSend(self, title: str, classification: Classification, contents: str = None):
        """
        Sends a log entry with predefined classification values, setting an error flag if the log level is critical.

        Args:
            title (str): The title of the log entry.
            classification (Classification): An instance of Classification that categorizes the log.
            contents (str, optional): The main content or message of the log. Defaults to None.
        """

        body = {
          "application": self.application,
          "source": self.__source,
          "title": title,
          "category": classification.value[0],
          "category2": classification.value[1],
          "contents": contents,
          "SYSLOG_LEVEL": classification.value[2].value
        }

        if classification.value[2].value < 0 or classification.value[2].value > 7:
            raise ValueError("Syslog Level must be between 0 and 7")
        if classification.value[2].value <= 3:
            self.__hadError = True
        self.__send(body)

    def fullSend(self, title: str, category: str, category2: str, syslogLevel: SyslogLevel, contents: str):
        """
        Sends a log entry with fully specified details, setting an error flag if the log level is critical.

        Args:
            title (str): The title of the log entry.
            category (str): Primary category of the log.
            category2 (str): Secondary category of the log.
            syslogLevel (SyslogLevel): The system log level (SYSLOG level code) of the entry.
            contents (str): The main content or message of the log.
        """
        body = {
            "application": self.application,
            "source": self.__source,
            "title": title,
            "category": category,
            "category2": category2,
            "contents": contents,
            "SYSLOG_LEVEL": syslogLevel.value
        }

        if syslogLevel.value < 0 or syslogLevel.value > 7:
            raise ValueError("Syslog Level must be between 0 and 7")
        if syslogLevel.value <= 3:
            self.__hadError = True

        self.__send(body)

    def __send(self, body: dict):
        """
        Sends a log entry to the configured API endpoint as a JSON payload.

        Args:
            body (dict): The log entry data formatted as a dictionary.
        """

        # Fazendo a chamada POST

        requests.post(url=self.__api_url,
                      headers={ "Authorization": f"Bearer {self.__token}", "Content-Type": "application/json" },
                      json=body)

    def hadError(self) -> bool:
        """
        Checks if any error-level log entries have been recorded.

        Returns:
            bool: True if an error-level log was recorded, otherwise False.
        """
        return self.__hadError

    def resetErrorMark(self) -> None:
        """
        Resets the error tracking flag to False.
        """
        self.__hadError = False
