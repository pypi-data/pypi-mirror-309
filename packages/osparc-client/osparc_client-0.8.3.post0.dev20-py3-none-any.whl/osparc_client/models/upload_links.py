# coding: utf-8

"""
    osparc.io public API

    osparc-simcore public API specifications  # noqa: E501

    The version of the OpenAPI document: 0.7.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from osparc_client.configuration import Configuration


class UploadLinks(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'abort_upload': 'str',
        'complete_upload': 'str'
    }

    attribute_map = {
        'abort_upload': 'abort_upload',
        'complete_upload': 'complete_upload'
    }

    def __init__(self, abort_upload=None, complete_upload=None, local_vars_configuration=None):  # noqa: E501
        """UploadLinks - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._abort_upload = None
        self._complete_upload = None
        self.discriminator = None

        self.abort_upload = abort_upload
        self.complete_upload = complete_upload

    @property
    def abort_upload(self):
        """Gets the abort_upload of this UploadLinks.  # noqa: E501


        :return: The abort_upload of this UploadLinks.  # noqa: E501
        :rtype: str
        """
        return self._abort_upload

    @abort_upload.setter
    def abort_upload(self, abort_upload):
        """Sets the abort_upload of this UploadLinks.


        :param abort_upload: The abort_upload of this UploadLinks.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and abort_upload is None:  # noqa: E501
            raise ValueError("Invalid value for `abort_upload`, must not be `None`")  # noqa: E501

        self._abort_upload = abort_upload

    @property
    def complete_upload(self):
        """Gets the complete_upload of this UploadLinks.  # noqa: E501


        :return: The complete_upload of this UploadLinks.  # noqa: E501
        :rtype: str
        """
        return self._complete_upload

    @complete_upload.setter
    def complete_upload(self, complete_upload):
        """Sets the complete_upload of this UploadLinks.


        :param complete_upload: The complete_upload of this UploadLinks.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and complete_upload is None:  # noqa: E501
            raise ValueError("Invalid value for `complete_upload`, must not be `None`")  # noqa: E501

        self._complete_upload = complete_upload

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UploadLinks):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UploadLinks):
            return True

        return self.to_dict() != other.to_dict()
