# Copyright 2023 Katteli Inc.
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
import os
import inspect

from .mode import *
from .compare import Compare
from .errors import *
from .v1 import snapshot as snapshot_v1

__all__ = ["snapshot"]


def get_snapshot_filename(frame, path, id):
    """Return snapshot filename based on the snapshot id.

    The filename has the following format:

        <test file name>[.<id>].snapshot

    The file is created in the same folder as the test that calls the snapshot function
    unless custom `path` is specified.
    """
    frame_info = inspect.getframeinfo(frame)

    id_parts = [os.path.basename(frame_info.filename)]
    if id is not None:
        id_parts.append(str(id).lower())
    id_parts.append("snapshot")

    id = ".".join(id_parts)

    if path is None:
        path = os.path.join(os.path.dirname(frame_info.filename), "snapshots")

    if not os.path.exists(path):
        os.makedirs(path)

    filename = os.path.join(path, id)

    return filename


def snapshot(
    value,
    id=None,
    output=None,
    path=None,
    name="snapshot",
    encoder=repr,
    comment=None,
    mode=SNAPSHOT_MODE_CHECK | SNAPSHOT_MODE_UPDATE,
    version=snapshot_v1.VERSION,
    frame=None,
    compare=Compare.eq,
):
    """Compare value representation to a stored snapshot.

    If snapshot does not exist, assertion passes else
    representation of the value is compared to the stored snapshot.

    Snapshot files have format:

        <test file name>[.<id>].snapshot

    :param value: value to be used for snapshot
    :param id: unique id of the snapshot file, default: `None`
    :param output: function to output the representation of the value
    :param path: custom snapshot path, default: `./snapshots`
    :param name: name of the snapshot value inside the snapshots file, default: `snapshot`
    :param encoder: custom snapshot encoder, default: `repr`
    :param comment: (deprecated)
    :param mode: mode of operation: CHECK, UPDATE, REWRITE, default: CHECK | UPDATE
    :param version: snapshot version, default: snapshot_v1.VERSION
    :param frame: caller frame, default: `None`
    :param compare: custom comparison function, default: equals
    """
    if frame is None:
        frame = inspect.currentframe().f_back

    try:
        repr_value = encoder(value)
    except:
        raise ValueError(f"encoder '{encoder}' failed to encode: {value}")

    if output:
        output(repr_value)

    filename = get_snapshot_filename(frame=frame, path=path, id=id)

    if version == snapshot_v1.VERSION:
        return snapshot_v1(
            filename=filename,
            repr_value=repr_value,
            name=name,
            mode=mode,
            compare=compare,
        )

    raise ValueError(f"unsupported snapshot version: {version}")


# define snapshot mode flags
snapshot.CHECK = SNAPSHOT_MODE_CHECK
snapshot.UPDATE = SNAPSHOT_MODE_UPDATE
snapshot.REWRITE = SNAPSHOT_MODE_REWRITE

# define comparison functions
snapshot.COMPARE = Compare

# define supported versions
snapshot.VERSION_V1 = snapshot_v1.VERSION
