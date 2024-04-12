"""
Google Cloud environment information
"""
# standard library imports
import logging
import os

# current package imports
from .exceptions import EnvironmentVariableNotSetError

import dotenv

dotenv.load_dotenv()


class Secrets:
    """
    A data class for centralized information about the google cloud environment.
    """

    def get_environment_variable(self, env_var_name: str) -> str:
        """
        Returns the value of the specified environment variable.

        Parameters
        ----------
        env_var_name: str
            name of the environment variable

        Returns
        -------
        str
            value of the environment variable

        Raises
        ------
        KeyError
            if the environment variable does not exist
        """
        environment_variable = os.getenv(env_var_name, None)
        if environment_variable is None:
            err = "Environment variable '{}' is not set".format(env_var_name)
            logging.error(err)
            raise EnvironmentVariableNotSetError(err)
        else:
            return environment_variable

    @property
    def GCLOUD_PROJECT_ID(self) -> str:
        """
        Returns the id of the google cloud project.

        Parameters
        ----------
        None

        Returns
        -------
        str
            id of the google cloud project
        """
        return self.get_environment_variable("GCLOUD_PROJECT_ID")

    @property
    def GCLOUD_PROJECT_NAME(self) -> str:
        """
        Returns the name of the google cloud project.

        Parameters
        ----------
        None

        Returns
        -------
        str
            name of the google cloud project
        """
        return self.get_environment_variable("GCLOUD_PROJECT_NAME")

    @property
    def GCLOUD_SERVICE_ACCOUNT_EMAIL(self) -> str:
        """
        Returns the email of the google cloud service account.

        Parameters
        ----------
        None

        Returns
        -------
        str
            email of the google cloud service account
        """
        return self.get_environment_variable("GCLOUD_SERVICE_ACCOUNT_EMAIL")

    @property
    def GCLOUD_STORAGE_BUCKET_TRAINING_DATA(self) -> str:
        """
        Returns the name of the google cloud storage bucket storing training data.

        Parameters
        ----------
        None

        Returns
        -------
        str
            name of the google cloud storage private bucket
        """
        return self.get_environment_variable("GCLOUD_STORAGE_BUCKET_TRAINING_DATA")
