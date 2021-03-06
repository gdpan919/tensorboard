# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Information about histogram summaries."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tensorboard.plugins.histogram import plugin_data_pb2


PLUGIN_NAME = 'histograms'

# The most recent value for the `version` field of the
# `HistogramPluginData` proto.
PROTO_VERSION = 0


def create_summary_metadata(display_name, description):
  """Create a `tf.SummaryMetadata` proto for histogram plugin data.

  Returns:
    A `tf.SummaryMetadata` protobuf object.
  """
  content = plugin_data_pb2.HistogramPluginData(version=PROTO_VERSION)
  return tf.SummaryMetadata(
      display_name=display_name,
      summary_description=description,
      plugin_data=tf.SummaryMetadata.PluginData(
          plugin_name=PLUGIN_NAME,
          content=content.SerializeToString()))


def parse_plugin_metadata(content):
  """Parse summary metadata to a Python object.

  Arguments:
    content: The `content` field of a `SummaryMetadata` proto
      corresponding to the histogram plugin.

  Returns:
    A `HistogramPluginData` protobuf object.
  """
  if content == '{}' or content == b'{}':
    # Old-style JSON format. Equivalent to an all-default proto.
    return plugin_data_pb2.HistogramPluginData()
  else:
    result = plugin_data_pb2.HistogramPluginData()
    # TODO(@jart): Instead of converting to bytes, assert that the input
    # is a bytestring, and raise a ValueError otherwise...but only after
    # converting `PluginData`'s `content` field to have type `bytes`
    # instead of `string`.
    result.ParseFromString(tf.compat.as_bytes(content))
    if result.version == 0:
      return result
    else:
      tf.logging.warn(
          'Unknown metadata version: %s. The latest version known to '
          'this build of TensorBoard is %s; perhaps a newer build is '
          'available?', result.version, PROTO_VERSION)
      return result
