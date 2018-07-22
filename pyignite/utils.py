# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def is_iterable(value):
    """ Check if value is iterable. """
    try:
        iter(value)
        return True
    except TypeError:
        return False


def is_hinted(value):
    """
    Check if a value is a tuple of data item and its type hint.
    """
    return (
        isinstance(value, tuple)
        and len(value) == 2
        and isinstance(value[1], object)
    )


def int_overflow(value: int) -> int:
    """
    Simulates 32bit integer overflow.
    """
    return ((value ^ 0x80000000) & 0xffffffff) - 0x80000000


def unwrap_binary(conn, wrapped: tuple):
    """
    Unwrap wrapped BinaryObject and convert it to Python data.

    :param conn: connection to Ignite cluster,
    :param wrapped: WrappedDataObject value,
    :return: dict representing wrapped BinaryObject.
    """
    from pyignite.datatypes import BinaryObject

    blob, offset = wrapped
    mock_conn = conn.make_buffered(blob)
    mock_conn.pos = offset
    data_class, data_bytes = BinaryObject.parse(mock_conn)
    return BinaryObject.to_python(data_class.from_buffer_copy(data_bytes))
