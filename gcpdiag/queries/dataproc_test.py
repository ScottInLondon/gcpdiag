# Copyright 2021 Google LLC
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
"""Test code in dataproc.py."""

from unittest import mock

from gcpdiag import models
from gcpdiag.queries import apis_stub, dataproc

DUMMY_PROJECT_NAME = 'dataproc1'
NUMBER_OF_CLUSTERS_IN_DATAPROC_JSON_DUMP_FILE = 4


@mock.patch('gcpdiag.queries.apis.get_api', new=apis_stub.get_api_stub)
class TestDataproc:
  """Test Dataproc"""

  def test_get_clusters(self):
    context = models.Context(project_id=DUMMY_PROJECT_NAME)
    clusters = dataproc.get_clusters(context)
    assert len(clusters) == NUMBER_OF_CLUSTERS_IN_DATAPROC_JSON_DUMP_FILE
    assert ('good', True) in [(c.name, c.is_running()) for c in clusters]

  def test_stackdriver_logging_enabled(self):
    context = models.Context(project_id=DUMMY_PROJECT_NAME)
    clusters = dataproc.get_clusters(context)
    for c in clusters:
      # In cluster logging-enable-true
      # dataproc:dataproc.logging.stackdriver.job.driver.enable is set
      # and equals "true"
      if c.name == 'logging-enable-true':
        assert c.is_stackdriver_logging_enabled()

      # In cluster logging-enable-false
      # dataproc:dataproc.logging.stackdriver.job.driver.enable is set
      # and equals "false"
      if c.name == 'logging-enable-false':
        assert not c.is_stackdriver_logging_enabled()

      # In cluster logging-enable-not-set
      # dataproc:dataproc.logging.stackdriver.job.driver.enable is not set
      if c.name == 'logging-enable-not-set':
        assert not c.is_stackdriver_logging_enabled()
