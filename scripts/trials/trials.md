## ALL LAYERS

| # | Layers | Mining Time | Min Support | Min Nodes | Dataset | Total Models | Patterns found | Top 3 Patterns |
|---|--------|-------------|-------------|-----------|---------|--------------|----------------|----------------|
| trial_0 | all_layers | 900 s | 10 | 8 | 50_200 | 100 | 5320 | ![14_0.png](./all_layers/trial_0/imgs-top3/14_0.png) ![15_5310.png](./all_layers/trial_0/imgs-top3/15_5310.png) ![15_5311.png](./all_layers/trial_0/imgs-top3/15_5311.png) |
| trial_1 | all_layers | 900 s | 20 | 8 | 50_200 | 200 | 4349 | ![35_5.png](./all_layers/trial_1/imgs-top3/35_5.png) ![36_607.png](./all_layers/trial_1/imgs-top3/36_607.png) ![38_81.png](./all_layers/trial_1/imgs-top3/38_81.png) |
| trial_2 | all_layers | 900 s | 30 | 8 | 50_200 | 300 | 485 | ![45_37.png](./all_layers/trial_2/imgs-top3/45_37.png) ![45_6.png](./all_layers/trial_2/imgs-top3/45_6.png) ![46_112.png](./all_layers/trial_2/imgs-top3/46_112.png) |
| trial_3 | all_layers | 900 s | 40 | 8 | 50_200 | 400 | 7 | ![53_6.png](./all_layers/trial_3/imgs-top3/53_6.png) ![67_5.png](./all_layers/trial_3/imgs-top3/67_5.png) ![68_4.png](./all_layers/trial_3/imgs-top3/68_4.png) |
| trial_4 | all_layers | 300 s | 10 | 4 | 100_500 | 229 | 34 | ![23_10.png](./all_layers/trial_4/imgs-top3/23_10.png) ![26_9.png](./all_layers/trial_4/imgs-top3/26_9.png) ![31_0.png](./all_layers/trial_4/imgs-top3/31_0.png) |
| trial_5 | all_layers | 1800 s | 8 | 4 | 100_500 | 229 | 57 | ![23_44.png](./all_layers/trial_5/imgs-top3/23_44.png) ![26_43.png](./all_layers/trial_5/imgs-top3/26_43.png) ![31_0.png](./all_layers/trial_5/imgs-top3/31_0.png) |
| trial_6 | all_layers | 300 s | 5 | 4 | 100_500 + 200_500 | 292 | 258 | ![18_255.png](./all_layers/trial_6/imgs-top3/18_255.png) ![23_5.png](./all_layers/trial_6/imgs-top3/23_5.png) ![25_254.png](./all_layers/trial_6/imgs-top3/25_254.png) |
| trial_7 | all_layers | 300 s | 5 | 4 | 100_1000 | 245 | 221 | ![19_216.png](./all_layers/trial_7/imgs-top3/19_216.png) ![20_133.png](./all_layers/trial_7/imgs-top3/20_133.png) ![26_213.png](./all_layers/trial_7/imgs-top3/26_213.png) |
| trial_8 | all_layers | 3600 s | 5 | 4 | 100_1000 | 245 | 330 | ![19_216.png](./all_layers/trial_8/imgs-top3/19_216.png) ![20_133.png](./all_layers/trial_8/imgs-top3/20_133.png) ![26_213.png](./all_layers/trial_8/imgs-top3/26_213.png) |
| trial_9 | all_layers, no application layer | 3600 s | 5 | 4 | 100_1000 | 245 | 748 | ![34_44.png](./all_layers/trial_9/imgs-top3/34_44.png) ![40_9.png](./all_layers/trial_9/imgs-top3/40_9.png) ![41_722.png](./all_layers/trial_9/imgs-top3/41_722.png) |


## SINGLE LAYERS

| # | Layers | Mining Time | Min Support | Min Nodes | Dataset | Total Models | Patterns found |
|---|--------|-------------|-------------|-----------|---------|--------------|----------------|
| 0 | application_layer | 900 seconds | 20 | 8 | 50_200 | 300 | 6 |
| 1 | business_layer | 900 seconds | 20 | 8 | 50_200 | 300 | 332 |
| 2 | motivation_layer | 900 seconds | 10 | 4 | 50_200 | 300 | 42 |
| 3 | strategy_layer | 900 seconds | 8 | 4 | 50_200 | 300 | 3 |
| 4 | technology_layer | 900 seconds | 8 | 4 | 50_200 | 300 | 240 |
| 5 | technology_layer | 900 seconds | 20 | 4 | 50_200 | 300 | 14 |
| 6 | motivation_layer | 300 seconds | 10 | 4 | 100_500 | 229 | 168 |
| 7 | motivation_layer | 300 seconds | 10 | 4 | 100_500 + 200_500 | 292 | 415 |
| 8 | business_layer | 3600 seconds | 60 | 4 | 100_1000 | 292 | 38 |

## COMBINED LAYERS

| # | Layers | Mining Time | Min Support | Min Nodes | Dataset | Total Models | Patterns found |
|---|--------|-------------|-------------|-----------|---------|--------------|----------------|
| 0 | business + application | 900 seconds | 10 | 8 | 50_200 | 300 | 503 |
| 0 | business + application | 900 seconds | 10 | 12 | 50_200 | 300 | 7 |
| 0 | business + strategy | 900 seconds | 20 | 8 | 50_200 | 300 | 449 |
| 0 | business + motivation | 900 seconds | 10 | 8 | 50_200 | 300 | 30 |
| 0 | business + application + technology | 1800 seconds | 10 | 6 | 100_1000 | 245 | 53 |
| 1 | application + technology | 900 seconds | 20 | 8 | 50_200 | 300 | 13 |
| 1 | application + motivation | 900 seconds | 20 | 8 | 50_200 | 300 | 6 |
| 1 | application + technology + physical | 900 seconds | 20 | 8 | 50_200 | 300 | 13 |
| 1 | application + technology + physical | 900 seconds | 10 | 8 | 50_200 | 300 | 33 |
| 1 | application + technology + other | 900 seconds | 8 | 6 | 100_1000 | 245 | 211 |
| 2 | motivation + strategy | 900 seconds | 10 | 6 | 50_200 | 300 | 0 |
| 3 | implementation & migration + physical + technology | 900 seconds | 10 | 8 | 50_200 | 300 | 28 |
| 3 | implementation & migration + motivation + other + strategy | 900 seconds | 10 | 8 | 50_200 | 300 | 0 |
| 2 | technology + physical + implementation_migration | 900 seconds | 8 | 6 | 100_1000 | 245 | 56 |
| 3 | motivation + strategy + other | 900 seconds | 8 | 6 | 100_1000 | 245 | 1 |
| 4 | application + technology + physical | 900 seconds | 10 | 8 | 100_1000 | 245 | 22 |
| 5 | motivation + strategy + other + implementation_migration | 900 seconds | 8 | 8 | 100_1000 | 245 | 0 |
