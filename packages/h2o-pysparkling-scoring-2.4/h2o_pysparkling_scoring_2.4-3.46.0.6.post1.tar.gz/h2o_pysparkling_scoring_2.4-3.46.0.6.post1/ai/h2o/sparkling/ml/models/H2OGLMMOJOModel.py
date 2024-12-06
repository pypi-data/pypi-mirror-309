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

from ai.h2o.sparkling.ml.params.H2OMOJOModelParams import H2OSupervisedMOJOModelParams
from pyspark.ml.util import _jvm
from py4j.java_gateway import JavaObject
from ai.h2o.sparkling.Initializer import Initializer
from ai.h2o.sparkling.ml.models.H2OMOJOSettings import H2OMOJOSettings
from ai.h2o.sparkling.ml.params.H2OTypeConverters import H2OTypeConverters
from ai.h2o.sparkling.H2ODataFrameConverters import H2ODataFrameConverters
from ai.h2o.sparkling.ml.params.HasIgnoredColsOnMOJO import HasIgnoredColsOnMOJO


class H2OGLMMOJOModel(H2OSupervisedMOJOModelParams, HasIgnoredColsOnMOJO):

    @staticmethod
    def createFromMojo(pathToMojo, settings=H2OMOJOSettings.default()):
        # We need to make sure that Sparkling Water classes are available on the Spark driver and executor paths
        Initializer.load_sparkling_jar()
        javaModel = _jvm().ai.h2o.sparkling.ml.models.H2OGLMMOJOModel.createFromMojo(pathToMojo, settings.toJavaObject())
        return H2OGLMMOJOModel(javaModel)


    def getCrossValidationModels(self):
        cvModels = self._java_obj.getCrossValidationModelsAsArray()
        if cvModels is None:
            return None
        elif isinstance(cvModels, JavaObject):
            return [H2OGLMMOJOModel(v) for v in cvModels]
        else:
            raise TypeError("Invalid type.")


    def getSeed(self):
        value = self._java_obj.getSeed()
        return value


    def getFamily(self):
        value = self._java_obj.getFamily()
        return value


    def getTweedieVariancePower(self):
        value = self._java_obj.getTweedieVariancePower()
        return value


    def getDispersionLearningRate(self):
        value = self._java_obj.getDispersionLearningRate()
        return value


    def getTweedieLinkPower(self):
        value = self._java_obj.getTweedieLinkPower()
        return value


    def getTheta(self):
        value = self._java_obj.getTheta()
        return value


    def getSolver(self):
        value = self._java_obj.getSolver()
        return value


    def getAlphaValue(self):
        value = self._java_obj.getAlphaValue()
        return H2OTypeConverters.scalaArrayToPythonArray(value)


    def getLambdaValue(self):
        value = self._java_obj.getLambdaValue()
        return H2OTypeConverters.scalaArrayToPythonArray(value)


    def getLambdaSearch(self):
        value = self._java_obj.getLambdaSearch()
        return value


    def getEarlyStopping(self):
        value = self._java_obj.getEarlyStopping()
        return value


    def getNlambdas(self):
        value = self._java_obj.getNlambdas()
        return value


    def getScoreIterationInterval(self):
        value = self._java_obj.getScoreIterationInterval()
        return value


    def getStandardize(self):
        value = self._java_obj.getStandardize()
        return value


    def getColdStart(self):
        value = self._java_obj.getColdStart()
        return value


    def getMissingValuesHandling(self):
        value = self._java_obj.getMissingValuesHandling()
        return value


    def getInfluence(self):
        value = self._java_obj.getInfluence()
        return value


    def getNonNegative(self):
        value = self._java_obj.getNonNegative()
        return value


    def getMaxIterations(self):
        value = self._java_obj.getMaxIterations()
        return value


    def getBetaEpsilon(self):
        value = self._java_obj.getBetaEpsilon()
        return value


    def getObjectiveEpsilon(self):
        value = self._java_obj.getObjectiveEpsilon()
        return value


    def getGradientEpsilon(self):
        value = self._java_obj.getGradientEpsilon()
        return value


    def getObjReg(self):
        value = self._java_obj.getObjReg()
        return value


    def getLink(self):
        value = self._java_obj.getLink()
        return value


    def getDispersionParameterMethod(self):
        value = self._java_obj.getDispersionParameterMethod()
        return value


    def getStartval(self):
        value = self._java_obj.getStartval()
        return H2OTypeConverters.scalaArrayToPythonArray(value)


    def getCalcLike(self):
        value = self._java_obj.getCalcLike()
        return value


    def getGenerateVariableInflationFactors(self):
        value = self._java_obj.getGenerateVariableInflationFactors()
        return value


    def getIntercept(self):
        value = self._java_obj.getIntercept()
        return value


    def getBuildNullModel(self):
        value = self._java_obj.getBuildNullModel()
        return value


    def getFixDispersionParameter(self):
        value = self._java_obj.getFixDispersionParameter()
        return value


    def getInitDispersionParameter(self):
        value = self._java_obj.getInitDispersionParameter()
        return value


    def getPrior(self):
        value = self._java_obj.getPrior()
        return value


    def getLambdaMinRatio(self):
        value = self._java_obj.getLambdaMinRatio()
        return value


    def getMaxActivePredictors(self):
        value = self._java_obj.getMaxActivePredictors()
        return value


    def getInteractions(self):
        value = self._java_obj.getInteractions()
        return H2OTypeConverters.scalaArrayToPythonArray(value)


    def getBalanceClasses(self):
        value = self._java_obj.getBalanceClasses()
        return value


    def getClassSamplingFactors(self):
        value = self._java_obj.getClassSamplingFactors()
        return H2OTypeConverters.scalaArrayToPythonArray(value)


    def getMaxAfterBalanceSize(self):
        value = self._java_obj.getMaxAfterBalanceSize()
        return value


    def getMaxConfusionMatrixSize(self):
        value = self._java_obj.getMaxConfusionMatrixSize()
        return value


    def getComputePValues(self):
        value = self._java_obj.getComputePValues()
        return value


    def getFixTweedieVariancePower(self):
        value = self._java_obj.getFixTweedieVariancePower()
        return value


    def getRemoveCollinearCols(self):
        value = self._java_obj.getRemoveCollinearCols()
        return value


    def getDispersionEpsilon(self):
        value = self._java_obj.getDispersionEpsilon()
        return value


    def getTweedieEpsilon(self):
        value = self._java_obj.getTweedieEpsilon()
        return value


    def getMaxIterationsDispersion(self):
        value = self._java_obj.getMaxIterationsDispersion()
        return value


    def getGenerateScoringHistory(self):
        value = self._java_obj.getGenerateScoringHistory()
        return value


    def getInitOptimalGlm(self):
        value = self._java_obj.getInitOptimalGlm()
        return value


    def getSeparateLinearBeta(self):
        value = self._java_obj.getSeparateLinearBeta()
        return value


    def getConstraintEta0(self):
        value = self._java_obj.getConstraintEta0()
        return value


    def getConstraintTau(self):
        value = self._java_obj.getConstraintTau()
        return value


    def getConstraintAlpha(self):
        value = self._java_obj.getConstraintAlpha()
        return value


    def getConstraintBeta(self):
        value = self._java_obj.getConstraintBeta()
        return value


    def getConstraintC0(self):
        value = self._java_obj.getConstraintC0()
        return value


    def getNfolds(self):
        value = self._java_obj.getNfolds()
        return value


    def getKeepCrossValidationModels(self):
        value = self._java_obj.getKeepCrossValidationModels()
        return value


    def getKeepCrossValidationPredictions(self):
        value = self._java_obj.getKeepCrossValidationPredictions()
        return value


    def getKeepCrossValidationFoldAssignment(self):
        value = self._java_obj.getKeepCrossValidationFoldAssignment()
        return value


    def getLabelCol(self):
        value = self._java_obj.getLabelCol()
        return value


    def getWeightCol(self):
        value = self._java_obj.getWeightCol()
        return value


    def getFoldCol(self):
        value = self._java_obj.getFoldCol()
        return value


    def getFoldAssignment(self):
        value = self._java_obj.getFoldAssignment()
        return value


    def getIgnoreConstCols(self):
        value = self._java_obj.getIgnoreConstCols()
        return value


    def getScoreEachIteration(self):
        value = self._java_obj.getScoreEachIteration()
        return value


    def getCheckpoint(self):
        value = self._java_obj.getCheckpoint()
        return value


    def getStoppingRounds(self):
        value = self._java_obj.getStoppingRounds()
        return value


    def getMaxRuntimeSecs(self):
        value = self._java_obj.getMaxRuntimeSecs()
        return value


    def getStoppingMetric(self):
        value = self._java_obj.getStoppingMetric()
        return value


    def getStoppingTolerance(self):
        value = self._java_obj.getStoppingTolerance()
        return value


    def getGainsliftBins(self):
        value = self._java_obj.getGainsliftBins()
        return value


    def getCustomMetricFunc(self):
        value = self._java_obj.getCustomMetricFunc()
        return value


    def getExportCheckpointsDir(self):
        value = self._java_obj.getExportCheckpointsDir()
        return value


    def getAucType(self):
        value = self._java_obj.getAucType()
        return value

    # Outputs

