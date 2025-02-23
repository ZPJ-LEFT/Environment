# LoRA: Low-Rank adaptation of large language models

## 摘要
在大规模预训练数据集上预训练，再在特定数据集上微调，是目前通用的技术方案。但对于大模型例如GPT-3 175B而言，在整个模型上重训练是负担沉重的，本文提出LoRA，固定预训练模型权重并注入可训练的Rank decomposition matrices(秩分解矩阵)到Transformer的每一层。

优点：
（1）LoRA可以将训练参数减少到10000倍，GPU内存需求降低三倍。
（2）相较于Adapters，LoRA不存在额外的推理延迟。

## 引言

Adapter方法拓展了网络深度，且性能无法与完全微调相比。

## 方法

更新权重:
```
W = W0 + dW
```

将dW(D×K)拆为A(D×r)、B(r×K)两个低秩矩阵，从而使待更新参数量衰减为r×(D+K)<<(D×K)
