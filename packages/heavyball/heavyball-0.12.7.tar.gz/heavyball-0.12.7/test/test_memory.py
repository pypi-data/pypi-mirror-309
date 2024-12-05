import pytest
import torch
from torch import nn

import heavyball
import heavyball.utils
from benchmark.utils import get_optim
from heavyball.utils import clean, set_torch


def get_memory():
    clean()
    torch.cuda.synchronize()
    clean()
    torch.cuda.synchronize()
    return torch.cuda.memory_allocated()


expected_memory = {'adamw': {'after': 4, 'peak': 5.1}, 'soap': {'after': 7, 'peak': 14},
                   'psgd': {'after': 4, 'peak': 10.5},
                   'padam': {'after': 5, 'peak': 11.4}}


@pytest.mark.parametrize("opt", ['ForeachPaLMPAdam', 'ForeachPSGDKron'])
@pytest.mark.parametrize("method", ['qr', 'newtonschulz2', 'svd', 'eigh'])
@pytest.mark.parametrize("size,depth", [(8192, 1), (2048, 16)])
def test_memory(opt, method, size, depth: int, iterations: int = 5):
    if 'soap' not in opt.lower() and method != 'qr':
        return
    set_torch()

    for k, v in expected_memory.items():
        if k in opt.lower():
            break
    else:
        raise ValueError(f'Unknown optimizer {opt}')

    opt = getattr(heavyball, opt)
    heavyball.utils.zeroth_power_mode = method

    torch.cuda.reset_peak_memory_stats()
    torch.cuda.reset_max_memory_allocated()
    torch.cuda.reset_max_memory_cached()
    torch.cuda.reset_accumulated_memory_stats()

    for i in range(iterations):
        model = nn.Sequential(*[nn.Linear(size, size) for _ in range(depth)]).cuda()

        model_allocated = get_memory()
        o = get_optim(opt, model.parameters(), lr=1e-3)
        model(torch.randn((1, size)).cuda()).sum().backward()
        o.step()

        opt_allocated = get_memory()
        o.zero_grad()

        del model, o
        peak = torch.cuda.memory_stats()['allocated_bytes.all.peak']

        print(f'Peak: {peak / model_allocated:.2f}x | Opt: {opt_allocated / model_allocated:.2f}x')
        if i > 0:
            assert peak / model_allocated < v['peak']
            assert opt_allocated / model_allocated < v['after']
