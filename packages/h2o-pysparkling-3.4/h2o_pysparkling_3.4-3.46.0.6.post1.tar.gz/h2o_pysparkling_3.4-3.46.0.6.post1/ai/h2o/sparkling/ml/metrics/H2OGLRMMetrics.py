#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from pyspark.ml.param import *
from ai.h2o.sparkling.ml.params.H2OTypeConverters import H2OTypeConverters
from ai.h2o.sparkling.H2ODataFrameConverters import H2ODataFrameConverters
from ai.h2o.sparkling.ml.metrics.H2OCommonMetrics import H2OCommonMetrics


class H2OGLRMMetrics(H2OCommonMetrics):

    def __init__(self, java_obj):
        self._java_obj = java_obj

    def getNumErr(self):
        """
        Sum of Squared Error (Numeric Cols).
        """
        value = self._java_obj.getNumErr()
        return value

    def getCatErr(self):
        """
        Misclassification Error (Categorical Cols).
        """
        value = self._java_obj.getCatErr()
        return value

    def getNumCnt(self):
        """
        Number of Non-Missing Numeric Values.
        """
        value = self._java_obj.getNumCnt()
        return value

    def getCatCnt(self):
        """
        Number of Non-Missing Categorical Values.
        """
        value = self._java_obj.getCatCnt()
        return value
