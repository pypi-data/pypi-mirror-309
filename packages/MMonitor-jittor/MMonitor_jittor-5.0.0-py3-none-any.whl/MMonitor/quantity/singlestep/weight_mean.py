from .base_class import SingleStepQuantity

import jittor as jt

class WeightMean(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.weight
        data = jt.flatten(data)
        return jt.mean(data)
