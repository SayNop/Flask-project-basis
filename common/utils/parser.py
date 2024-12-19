try:
    from collections.abc import MutableSequence
except ImportError:
    from collections import MutableSequence
from flask_restful import current_app, abort
from flask_restful.reqparse import Argument, six, _friendly_location

from .response import PARAMS_ERROR


class CustomArgument(Argument):

    # ** convert '' to None
    def convert(self, value, op):
        # pass ''
        if self.nullable and not self.required and value in [None, '']:
            return None
        return super().convert(value, op)

    def parse(self, request, bundle_errors=False):
        source = self.source(request)

        results = []

        # Sentinels
        _not_found = False
        _found = True

        for operator in self.operators:
            name = self.name + operator.replace("=", "", 1)
            if name in source:
                # Account for MultiDict and regular dict
                if hasattr(source, "getlist"):
                    values = source.getlist(name)
                else:
                    values = source.get(name)
                    if not (isinstance(values, MutableSequence) and self.action == 'append'):
                        values = [values]

                for value in values:
                    if hasattr(value, "strip") and self.trim:
                        value = value.strip()
                    if hasattr(value, "lower") and not self.case_sensitive:
                        value = value.lower()

                        if hasattr(self.choices, "__iter__"):
                            self.choices = [choice.lower()
                                            for choice in self.choices]

                    try:
                        value = self.convert(value, operator)
                    except Exception as error:
                        if self.ignore:
                            continue
                        return self.handle_validation_error(error, bundle_errors)
                    # ** Choices validation for non-empty values
                    if self.choices and (self.required or not self.nullable):
                        if value not in self.choices:
                            if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
                                return self.handle_validation_error(
                                    ValueError(u"{0} is not a valid choice".format(
                                        value)), bundle_errors)
                            self.handle_validation_error(
                                ValueError(u"{0} is not a valid choice".format(
                                    value)), bundle_errors)

                    if name in request.unparsed_arguments:
                        request.unparsed_arguments.pop(name)
                    results.append(value)

        if not results and self.required:
            if isinstance(self.location, six.string_types):
                error_msg = u"Missing required parameter in {0}".format(
                    _friendly_location.get(self.location, self.location)
                )
            else:
                friendly_locations = [_friendly_location.get(loc, loc)
                                      for loc in self.location]
                error_msg = u"Missing required parameter in {0}".format(
                    ' or '.join(friendly_locations)
                )
            if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
                return self.handle_validation_error(ValueError(error_msg), bundle_errors)
            self.handle_validation_error(ValueError(error_msg), bundle_errors)

        if not results:
            if callable(self.default):
                return self.default(), _not_found
            else:
                return self.default, _not_found

        if self.action == 'append':
            return results, _found

        if self.action == 'store' or len(results) == 1:
            return results[0], _found
        return results, _found

    # ** custom response format
    def handle_validation_error(self, error, bundle_errors):
        error_str = six.text_type(error)
        error_msg = self.help.format(error_msg=error_str) if self.help else f'{self.name}:{error_str}'

        if bundle_errors:
            return error, error_msg
        # ** status_code & key,value in response json
        abort(400, code=PARAMS_ERROR, success=False, message=error_msg)


def mobile(mobile_str):
    """
    mobile format
    :param mobile_str: input str
    :return: mobile_str
    """
    import re
    if re.match(r'^1[3-9]\d{9}$', mobile_str):
        return mobile_str
    else:
        raise ValueError('{} is not a valid mobile'.format(mobile_str))


class str_len_range(object):
    """
    String length check
    :params low: min length
    :params high: max length
    :params value: check string
    """
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def __call__(self, value):
        if type(value) != str or len(value) < self.low or len(value) > self.high:
            raise ValueError(f'{value} exception，string length range {self.low}-{self.high}')
        return value


def ip_address(ip_str):
    """
    ip address check
    :param ip_str: input str
    :return: ip_address_str
    """
    import re
    if re.match(r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$', ip_str):
        return ip_str
    raise ValueError(f'{ip_str} is in an illegal IP address format！')
