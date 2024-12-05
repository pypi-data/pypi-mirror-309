# HeavyBall

> [!IMPORTANT]  
> The SOAP implementation was broken until 0.9.0. Please upgrade to 0.9.0 or later.

A simple package of efficient optimizers

The goal is not to thrive for completeness, full maintenance or abstraction, but instead to provide a simple
largely static alternative to `torch.optim` with more and better optimizers.

Currently (2024-11-13, 0.12.5), the recommended stable optimizer is `PrecondSchedulePaLMForeachSOAP` (see below). The
recommended experimental optimizer is `ForeachPSGDKron`.

## Features

* **Stochastic Rounding**: [FP32 convergence with BF16 parameters](https://github.com/pytorch/pytorch/issues/120376)
* **Inplace EMA**: Same math, but less memory, less compute and higher stability
* **Foreach**: Fast multi-tensor application
* **PaLM Beta2**: Fast initial
  convergence, [stable late convergence](https://x.com/_clashluke/status/1820810798693818761)
* **ScheduleFree**: No learning rate schedule, but better convergence
* [**Preconditioner Schedule**](https://github.com/lixilinx/psgd_torch/): Improved loss-per-step in early convergence,
  better step-per-second in late convergence (explained below)

## Getting started

```bash
pip install heavyball
```

```python
import torch
import heavyball

# Create a model
model = torch.nn.Linear(16, 1)

# Create an optimizer
optimizer = heavyball.PrecondSchedulePaLMForeachSOAP(model.parameters(), lr=1e-3)

x = torch.randn(128, 16)
y = torch.randn(128, 1)

for _ in range(1000):
    optimizer.zero_grad()
    loss = torch.nn.functional.mse_loss(model(x), y)
    loss.backward()
    optimizer.step()
```

## Optimizers

| Name                                 | Description                                                                                                                                                       | Advantages / Disadvantages                                                                                                                                                                                                                                                                                                            |
|--------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ForeachAdamW**                     | More efficient (speed, memory) [AdamW](https://arxiv.org/abs/1711.05101)                                                                                          | + Faster than AdamW<br>+ Possibly more (numerically) stable                                                                                                                                                                                                                                                                           
| **ForeachLaProp**                    | More efficient (speed, memory) [LaProp](https://arxiv.org/abs/2002.04839)                                                                                         | + Same cost as AdamW<br>+ Marginally better converence (better proofs)<br>+ Higher hyperparameter stability<br>- Not a guaranteed win (can be neutral)<br>- No "Slingshot"                                                                                                                                                            |
| **ForeachADOPT**                     | More efficient (speed, memory) [ADOPT](https://arxiv.org/abs/2411.02853)                                                                                          | + Same cost as AdamW<br>+ Rigorous mathematical convergence proofs, even for challenging models (GANs)<br>- Empirically underperforms LaProp<br>- no bf16                                                                                                                                                                             |
| **ForeachSFAdamW**                   | More efficient (speed, memory) [ScheduleFree AdamW](https://arxiv.org/abs/2405.15682)                                                                             | + Same cost as AdamW, but better eval perf<br>+ Full control over hyperparameters                                                                                                                                                                                                                                                     |
| **PaLMForeachSFAdamW**               | ForeachSFAdamW with [PaLM's beta2 schedule](https://arxiv.org/abs/2204.02311)                                                                                     | + Same cost as AdamW, but better eval perf<br>+ Less control, but faster early and more stable late convergence<br>+ ScheduleFree<br>- slow early convergence                                                                                                                                                                         |
| **ForeachSOAP**                      | More efficient (speed, memory) [SOAP](https://arxiv.org/abs/2409.11321)                                                                                           | + Faster convergence (loss-at-step)<br>+ Full control over hyperparameters<br>- more memory usage<br>- more hyperparameters<br>- higher overhead than AdamW (can be ammortized; better loss-at-second)                                                                                                                                |
| **PaLMForeachSOAP**                  | ForeachSOAP with [PaLM's beta2 schedule](https://arxiv.org/abs/2204.02311)                                                                                        | + Faster convergence (loss-at-step)<br>+ Less control, but faster early and more stable late convergence<br>- more memory usage<br>- more hyperparameters<br>- higher overhead than AdamW (can be ammortized; better loss-at-second)                                                                                                  |
| **SFPaLMForeachSOAP**                | ScheduleFree PaLMForeachSOAP                                                                                                                                      | + Fast convergence (loss-at-step)<br>+ less memory usage than PaLMForeachSOAP (more tham AdamW)<br>- slower initial convergence than PaLMForeachSOAP (but allows higher LRs)<br>- higher overhead than AdamW (can be ammortized)                                                                                                      |
| **PrecondScheduleSFPaLMForeachSOAP** | SFPaLMForeachSOAP with [preconditioner schedule](https://github.com/lixilinx/psgd_torch/), matching the error of PrecondEvery=2 with the cost of PrecondEvery=512 | + Better initial convergence than SFPaLMForeachSOAP<br>+ Significantly faster (sec/it) later<br>+ less memory usage than PaLMForeachSOAP (more tham AdamW)<br>- slower initial convergence than PaLMForeachSOAP (but allows higher LRs)<br>- higher overhead than AdamW (can be ammortized), goes to 0 with increasing number of step |
| **PrecondSchedulePaLMForeachSOAP**   | PrecondScheduleSFPaLMForeachSOAP without schedule-free                                                                                                            | + Best initial convergence<br>+ Significantly faster (sec/it) later<br>+ high stability<br>- more memory usage than PrecondScheduleSFPaLMForeachSOAP<br>- higher overhead than AdamW (can be ammortized), goes to 0 with increasing number of steps                                                                                   |
| **PrecondScheduleForeachSOAP**       | PrecondScheduleSFPaLMForeachSOAP without PaLM's beta2 schedule                                                                                                    | + Better initial convergence<br>+ Significantly faster (sec/it) later<br>- more memory usage than PrecondScheduleSFPaLMForeachSOAP<br>- higher overhead than AdamW (can be ammortized), goes to 0 with increasing number of steps                                                                                                     |

## Precond Schedule

The default preconditioner schedule (`f`) would yield the following update intervals:

| Steps     | Interval, `f` | Total (schedule) | Total (constant, every 2) | Total (constant, every 16) |
|-----------|---------------|------------------|---------------------------|----------------------------|
| 10        | 1.00005       | 10               | 5 (0.5x)                  | 0 (0.0x)                   |
| 100       | 1.026         | 99               | 50 (0.5x)                 | 6 (0.1x)                   |
| 1,000     | 2.0           | 738              | 500 (0.7x)                | 62 (0.1x)                  |
| 10,000    | 14.3          | 2,168            | 5,000 (2.3x)              | 625 (0.3x)                 |
| 100,000   | 100.2         | 4,049            | 50,000 (12.3x)            | 6,250 (1.5x)               |
| 1,000,000 | 513           | 7,245            | 500,000 (69.0x)           | 62,500 (8.6x)              |

## Utils

To access `heavyball.utils`, you need to explicitly `import heavyball.utils`.\
It has several handy functions:

* `set_torch()` sets pytorch optimization settings (TF32, opt_einsum, benchmark, ...)
* `compile_mode`, a string passed as-is to `torch.compile(mode=compile_mode)` in all compiled heavyball calls
* `zeroth_power_mode`, a string determining whether to use QR, newtonschulz{iterations}, or svd or eigh to approximate
  the eigenvectors. Eigh has the highest precision and cost