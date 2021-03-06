# Copyright 2019 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
PSO-Attack test.
"""
import numpy as np
import pytest

from mindspore import Tensor
import mindspore.nn as nn
from mindspore.nn import Cell
from mindspore import context

from mindarmour.adv_robustness.attacks import PSOAttack
from mindarmour import BlackModel


# for user
class ModelToBeAttacked(BlackModel):
    """model to be attack"""

    def __init__(self, network):
        super(ModelToBeAttacked, self).__init__()
        self._network = network

    def predict(self, inputs):
        """predict"""
        result = self._network(Tensor(inputs.astype(np.float32)))
        return result.asnumpy()


class SimpleNet(Cell):
    """
    Construct the network of target model.

    Examples:
        >>> net = SimpleNet()
    """

    def __init__(self):
        """
        Introduce the layers used for network construction.
        """
        super(SimpleNet, self).__init__()

        self._relu = nn.ReLU()

    def construct(self, inputs):
        """
        Construct network.

        Args:
            inputs (Tensor): Input data.
        """
        out = self._relu(inputs)
        return out


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_pso_attack():
    """
    PSO_Attack test
    """
    context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")
    batch_size = 6

    net = SimpleNet()
    inputs = np.random.rand(batch_size, 10)

    model = ModelToBeAttacked(net)
    labels = np.random.randint(low=0, high=10, size=batch_size)
    labels = np.eye(10)[labels]
    labels = labels.astype(np.float32)

    attack = PSOAttack(model, bounds=(0.0, 1.0), pm=0.5, sparse=False)
    _, adv_data, _ = attack.generate(inputs, labels)
    assert np.any(inputs != adv_data)


@pytest.mark.level0
@pytest.mark.platform_arm_ascend_training
@pytest.mark.platform_x86_ascend_training
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_pso_attack_targeted():
    """
    PSO_Attack test
    """
    context.set_context(mode=context.GRAPH_MODE, device_target="Ascend")
    batch_size = 6

    net = SimpleNet()
    inputs = np.random.rand(batch_size, 10)

    model = ModelToBeAttacked(net)
    labels = np.random.randint(low=0, high=10, size=batch_size)
    labels = np.eye(10)[labels]
    labels = labels.astype(np.float32)

    attack = PSOAttack(model, bounds=(0.0, 1.0), pm=0.5, targeted=True,
                       sparse=False)
    _, adv_data, _ = attack.generate(inputs, labels)
    assert np.any(inputs != adv_data)


@pytest.mark.level0
@pytest.mark.platform_x86_gpu_inference
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_pso_attack_gpu():
    """
    PSO_Attack test
    """
    context.set_context(device_target="GPU")
    batch_size = 6

    net = SimpleNet()
    inputs = np.random.rand(batch_size, 10)

    model = ModelToBeAttacked(net)
    labels = np.random.randint(low=0, high=10, size=batch_size)
    labels = np.eye(10)[labels]
    labels = labels.astype(np.float32)

    attack = PSOAttack(model, bounds=(0.0, 1.0), pm=0.5, sparse=False)
    _, adv_data, _ = attack.generate(inputs, labels)
    assert np.any(inputs != adv_data)


@pytest.mark.level0
@pytest.mark.platform_x86_cpu
@pytest.mark.env_card
@pytest.mark.component_mindarmour
def test_pso_attack_cpu():
    """
    PSO_Attack test
    """
    context.set_context(mode=context.GRAPH_MODE, device_target="CPU")
    batch_size = 6

    net = SimpleNet()
    inputs = np.random.rand(batch_size, 10)

    model = ModelToBeAttacked(net)
    labels = np.random.randint(low=0, high=10, size=batch_size)
    labels = np.eye(10)[labels]
    labels = labels.astype(np.float32)

    attack = PSOAttack(model, bounds=(0.0, 1.0), pm=0.5, sparse=False)
    _, adv_data, _ = attack.generate(inputs, labels)
    assert np.any(inputs != adv_data)
