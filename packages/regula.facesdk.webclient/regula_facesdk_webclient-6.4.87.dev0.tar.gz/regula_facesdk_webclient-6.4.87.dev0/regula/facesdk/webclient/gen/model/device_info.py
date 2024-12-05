# coding: utf-8

"""
    Regula Face SDK Web API

    <a href=\"https://regulaforensics.com/products/face-recognition-sdk/  \" target=\"_blank\">Regula Face SDK</a> is a cross-platform biometric verification solution for a digital identity verification process and image quality assurance. The SDK enables convenient and reliable face capture on the client side (mobile, web, and desktop) and further processing on the client or server side.   The Face SDK includes the following features:  * <a href=\"https://docs.regulaforensics.com/develop/face-sdk/overview/introduction/#face-detection\" target=\"_blank\">Face detection and image quality assessment</a> * <a href=\"https://docs.regulaforensics.com/develop/face-sdk/overview/introduction/#face-comparison-11\" target=\"_blank\">Face match (1:1)</a> * <a href=\"https://docs.regulaforensics.com/develop/face-sdk/overview/introduction/#face-identification-1n\" target=\"_blank\">Face search (1:N)</a> * <a href=\"https://docs.regulaforensics.com/develop/face-sdk/overview/introduction/#liveness-assessment\" target=\"_blank\">Liveness detection</a>  Here is the <a href=\"https://github.com/regulaforensics/FaceSDK-web-openapi  \" target=\"_blank\">OpenAPI specification on GitHub</a>.   ### Clients * [JavaScript](https://github.com/regulaforensics/FaceSDK-web-js-client) client for the browser and node.js based on axios * [Java](https://github.com/regulaforensics/FaceSDK-web-java-client) client compatible with jvm and android * [Python](https://github.com/regulaforensics/FaceSDK-web-python-client) 3.5+ client * [C#](https://github.com/regulaforensics/FaceSDK-web-csharp-client) client for .NET & .NET Core   # noqa: E501

    The version of the OpenAPI document: 6.2.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from regula.facesdk.webclient.gen.configuration import Configuration


class DeviceInfo(object):
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
        'app': 'str',
        'license_id': 'str, none_type',
        'license_serial': 'str, none_type',
        'license_valid_until': 'datetime, none_type',
        'version': 'str, none_type',
    }

    attribute_map = {
        'app': 'app',
        'license_id': 'licenseId',
        'license_serial': 'licenseSerial',
        'license_valid_until': 'licenseValidUntil',
        'version': 'version',
    }

    def __init__(self, app=None, license_id=None, license_serial=None, license_valid_until=None, version=None, local_vars_configuration=None):  # noqa: E501
        """DeviceInfo - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._app = None
        self._license_id = None
        self._license_serial = None
        self._license_valid_until = None
        self._version = None
        self.discriminator = None

        self.app = app
        self.license_id = license_id
        self.license_serial = license_serial
        self.license_valid_until = license_valid_until
        self.version = version

    @property
    def app(self):
        """Gets the app of this DeviceInfo.  # noqa: E501

        Application name.  # noqa: E501

        :return: The app of this DeviceInfo.  # noqa: E501
        :rtype: str
        """
        return self._app

    @app.setter
    def app(self, app):
        """Sets the app of this DeviceInfo.

        Application name.  # noqa: E501

        :param app: The app of this DeviceInfo.  # noqa: E501
        :type app: str
        """
        if self.local_vars_configuration.client_side_validation and app is None:  # noqa: E501
            raise ValueError("Invalid value for `app`, must not be `None`")  # noqa: E501

        self._app = app

    @property
    def license_id(self):
        """Gets the license_id of this DeviceInfo.  # noqa: E501

        Unique license identifier.  # noqa: E501

        :return: The license_id of this DeviceInfo.  # noqa: E501
        :rtype: str, none_type
        """
        return self._license_id

    @license_id.setter
    def license_id(self, license_id):
        """Sets the license_id of this DeviceInfo.

        Unique license identifier.  # noqa: E501

        :param license_id: The license_id of this DeviceInfo.  # noqa: E501
        :type license_id: str, none_type
        """

        self._license_id = license_id

    @property
    def license_serial(self):
        """Gets the license_serial of this DeviceInfo.  # noqa: E501

        License serial number.  # noqa: E501

        :return: The license_serial of this DeviceInfo.  # noqa: E501
        :rtype: str, none_type
        """
        return self._license_serial

    @license_serial.setter
    def license_serial(self, license_serial):
        """Sets the license_serial of this DeviceInfo.

        License serial number.  # noqa: E501

        :param license_serial: The license_serial of this DeviceInfo.  # noqa: E501
        :type license_serial: str, none_type
        """

        self._license_serial = license_serial

    @property
    def license_valid_until(self):
        """Gets the license_valid_until of this DeviceInfo.  # noqa: E501

        License validity date.  # noqa: E501

        :return: The license_valid_until of this DeviceInfo.  # noqa: E501
        :rtype: datetime, none_type
        """
        return self._license_valid_until

    @license_valid_until.setter
    def license_valid_until(self, license_valid_until):
        """Sets the license_valid_until of this DeviceInfo.

        License validity date.  # noqa: E501

        :param license_valid_until: The license_valid_until of this DeviceInfo.  # noqa: E501
        :type license_valid_until: datetime, none_type
        """

        self._license_valid_until = license_valid_until

    @property
    def version(self):
        """Gets the version of this DeviceInfo.  # noqa: E501

        Product version.  # noqa: E501

        :return: The version of this DeviceInfo.  # noqa: E501
        :rtype: str, none_type
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this DeviceInfo.

        Product version.  # noqa: E501

        :param version: The version of this DeviceInfo.  # noqa: E501
        :type version: str, none_type
        """

        self._version = version

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
        if not isinstance(other, DeviceInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DeviceInfo):
            return True

        return self.to_dict() != other.to_dict()
