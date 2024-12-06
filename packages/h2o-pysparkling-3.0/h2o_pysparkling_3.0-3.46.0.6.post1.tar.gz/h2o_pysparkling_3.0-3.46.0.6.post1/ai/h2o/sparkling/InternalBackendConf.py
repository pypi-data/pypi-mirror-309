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

import warnings
from ai.h2o.sparkling.SharedBackendConfUtils import SharedBackendConfUtils


class InternalBackendConf(SharedBackendConfUtils):

    #
    # Getters
    #

    def numH2OWorkers(self):
        return self._get_option(self._jconf.numH2OWorkers())

    def extraClusterNodes(self):
        return self._jconf.extraClusterNodes()

    def drddMulFactor(self):
        return self._jconf.drddMulFactor()

    def numRddRetries(self):
        return self._jconf.numRddRetries()

    def defaultCloudSize(self):
        return self._jconf.defaultCloudSize()

    def subseqTries(self):
        return self._jconf.subseqTries()

    def hdfsConf(self):
        return self._get_option(self._jconf.hdfsConf())

    def spreadRddRetriesTimeout(self):
        return self._jconf.spreadRddRetriesTimeout()

    def isDirectIpConfigurationEnabled(self):
        return self._jconf.isDirectIpConfigurationEnabled()

    def jettyLdapAesEncryptedBindPasswordLoginModuleKey(self):
        return self._get_option(self._jconf.jettyLdapAesEncryptedBindPasswordLoginModuleKey())

    def jettyLdapAesEncryptedBindPasswordLoginModuleIV(self):
        return self._get_option(self._jconf.jettyLdapAesEncryptedBindPasswordLoginModuleIV())


    #
    # Setters
    #

    def setNumH2OWorkers(self, numWorkers):
        self._jconf.setNumH2OWorkers(numWorkers)
        return self

    def setExtraClusterNodesEnabled(self):
        self._jconf.setExtraClusterNodesEnabled()
        return self

    def setExtraClusterNodesDisabled(self):
        self._jconf.setExtraClusterNodesDisabled()
        return self

    def setDrddMulFactor(self, factor):
        self._jconf.setDrddMulFactor(factor)
        return self

    def setNumRddRetries(self, retries):
        self._jconf.setNumRddRetries(retries)
        return self

    def setDefaultCloudSize(self, defaultClusterSize):
        self._jconf.setDefaultCloudSize(defaultClusterSize)
        return self

    def setSubseqTries(self, subseqTriesNum):
        self._jconf.setSubseqTries(subseqTriesNum)
        return self

    def setHdfsConf(self, *args):
        self._jconf.setHdfsConf(*args)
        return self

    def setSpreadRddRetriesTimeout(self, timeout):
        self._jconf.setSpreadRddRetriesTimeout(timeout)
        return self

    def setDirectIpConfigurationEnabled(self):
        self._jconf.setDirectIpConfigurationEnabled()
        return self

    def setDirectIpConfigurationDisabled(self):
        self._jconf.setDirectIpConfigurationDisabled()
        return self

    def setJettyLdapAesEncryptedBindPasswordLoginModuleKey(self, key):
        self._jconf.setJettyLdapAesEncryptedBindPasswordLoginModuleKey(key)
        return self

    def setJettyLdapAesEncryptedBindPasswordLoginModuleIV(self, iv):
        self._jconf.setJettyLdapAesEncryptedBindPasswordLoginModuleIV(iv)
        return self
