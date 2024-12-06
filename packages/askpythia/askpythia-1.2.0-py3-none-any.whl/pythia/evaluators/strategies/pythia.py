
from pythia.evaluators._evaluators import RedirectEvaluator
from pythia.evaluators.models import HostedModel
from pythia.evaluators.strategies.pythiav1 import PythiaV1Evaluator
from pythia.evaluators.strategies.pythiav2 import PythiaV2Evaluator


class PythiaEvaluator(RedirectEvaluator):
    def __init__(self, model: HostedModel):
        super().__init__(model, PythiaV1Evaluator(model), PythiaV2Evaluator(model))
