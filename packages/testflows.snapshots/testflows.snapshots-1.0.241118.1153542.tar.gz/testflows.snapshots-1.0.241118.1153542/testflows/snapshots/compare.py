# Copyright 2024 Katteli Inc.
# TestFlows.com Open-Source Software Testing Framework (http://testflows.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re
import operator


def _strip_single_quotes(value):
    """Strip single wrapping quotes if present."""
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value


class Compare:
    """Comparison functions."""

    eq = operator.eq
    ne = operator.ne
    lt = operator.lt
    le = operator.le
    gt = operator.gt
    ge = operator.ge

    @staticmethod
    def contains(a, b, strip_single_quotes=True):
        """Compare if a contains b.

        Strip single wrapping quotes if present
        to allow for string comparison when value is encoded
        with the default repr encoder.
        """
        if strip_single_quotes:
            b = _strip_single_quotes(b)
        return operator.contains(a, b)

    @staticmethod
    def resub(pattern, value="", op=operator.eq):
        """Compare after applying regular expression substitution."""
        pattern = re.compile(pattern)
        return lambda a, b: op(pattern.sub(value, a), pattern.sub(value, b))

    @staticmethod
    def rematch(pattern, strip_single_quotes=True):
        """Compare if matching regular expression pattern.

        Strip single wrapping quotes if present
        to allow for string comparison when value is encoded
        with the default repr encoder.
        """
        pattern = re.compile(pattern)

        def _compare(a, b):
            if strip_single_quotes:
                a = _strip_single_quotes(a)
                b = _strip_single_quotes(b)
            match_a = pattern.match(a)
            match_b = pattern.match(b)
            return match_a is not None and match_b is not None

        return _compare

    @staticmethod
    def renotmatch(pattern, strip_single_quotes=True):
        """Compare if not matching regular expression pattern.

        Strip single wrapping quotes if present
        to allow for string comparison when value is encoded
        with the default repr encoder.
        """

        pattern = re.compile(pattern)

        def _compare(a, b):
            if strip_single_quotes:
                a = _strip_single_quotes(a)
                b = _strip_single_quotes(b)
            match_a = pattern.match(a)
            match_b = pattern.match(b)
            return match_a is None and match_b is None

        return _compare
