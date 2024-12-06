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

from warnings import warn
from pyspark import keyword_only
from ai.h2o.sparkling.Initializer import Initializer
from ai.h2o.sparkling.ml.Utils import Utils
from ai.h2o.sparkling.ml.algos.H2OGLM import H2OGLM


class H2OGLMRegressor(H2OGLM):

    @keyword_only
    def __init__(self,
                 randomCols=None,
                 ignoredCols=None,
                 plugValues=None,
                 betaConstraints=None,
                 interactionPairs=None,
                 linearConstraints=None,
                 columnsToCategorical=[],
                 keepBinaryModels=False,
                 withContributions=False,
                 dataFrameSerializer="ai.h2o.sparkling.utils.JSONDataFrameSerializer",
                 withLeafNodeAssignments=False,
                 convertInvalidNumbersToNa=False,
                 detailedPredictionCol="detailed_prediction",
                 validationDataFrame=None,
                 featuresCols=[],
                 predictionCol="prediction",
                 convertUnknownCategoricalLevelsToNa=False,
                 splitRatio=1.0,
                 withStageResults=False,
                 seed=-1,
                 family="AUTO",
                 tweedieVariancePower=0.0,
                 dispersionLearningRate=0.5,
                 tweedieLinkPower=1.0,
                 theta=1.0E-10,
                 solver="AUTO",
                 alphaValue=None,
                 lambdaValue=None,
                 lambdaSearch=False,
                 earlyStopping=True,
                 nlambdas=-1,
                 scoreIterationInterval=-1,
                 standardize=True,
                 coldStart=False,
                 missingValuesHandling="MeanImputation",
                 influence=None,
                 nonNegative=False,
                 maxIterations=-1,
                 betaEpsilon=1.0E-4,
                 objectiveEpsilon=-1.0,
                 gradientEpsilon=-1.0,
                 objReg=-1.0,
                 link="family_default",
                 dispersionParameterMethod="pearson",
                 startval=None,
                 calcLike=False,
                 generateVariableInflationFactors=False,
                 intercept=True,
                 buildNullModel=False,
                 fixDispersionParameter=False,
                 initDispersionParameter=1.0,
                 prior=-1.0,
                 lambdaMinRatio=-1.0,
                 maxActivePredictors=-1,
                 interactions=None,
                 balanceClasses=False,
                 classSamplingFactors=None,
                 maxAfterBalanceSize=5.0,
                 maxConfusionMatrixSize=20,
                 computePValues=False,
                 fixTweedieVariancePower=True,
                 removeCollinearCols=False,
                 dispersionEpsilon=1.0E-4,
                 tweedieEpsilon=8.0E-17,
                 maxIterationsDispersion=3000,
                 generateScoringHistory=False,
                 initOptimalGlm=False,
                 separateLinearBeta=False,
                 constraintEta0=0.1258925,
                 constraintTau=10.0,
                 constraintAlpha=0.1,
                 constraintBeta=0.9,
                 constraintC0=10.0,
                 modelId=None,
                 nfolds=0,
                 keepCrossValidationModels=True,
                 keepCrossValidationPredictions=False,
                 keepCrossValidationFoldAssignment=False,
                 labelCol="label",
                 weightCol=None,
                 offsetCol=None,
                 foldCol=None,
                 foldAssignment="AUTO",
                 ignoreConstCols=True,
                 scoreEachIteration=False,
                 checkpoint=None,
                 stoppingRounds=0,
                 maxRuntimeSecs=0.0,
                 stoppingMetric="AUTO",
                 stoppingTolerance=0.001,
                 gainsliftBins=-1,
                 customMetricFunc=None,
                 exportCheckpointsDir=None,
                 aucType="AUTO"):
        Initializer.load_sparkling_jar()
        super(H2OGLM, self).__init__()
        self._java_obj = self._new_java_obj("ai.h2o.sparkling.ml.algos.regression.H2OGLMRegressor", self.uid)
        self._setDefaultValuesFromJava()
        kwargs = Utils.getInputKwargs(self)
        kwargs = self._updateInitKwargs(kwargs)

        if 'interactionPairs' in kwargs:
            warn("Interaction pairs are not supported!")
        self._set(**kwargs)
        self._transfer_params_to_java()
