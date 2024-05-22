## ALL LAYERS

| # | Layers | Mining Time | Min Support | Min Nodes | Dataset | Total Models | Patterns found |
|---|--------|-------------|-------------|-----------|---------|--------------|----------------|
| 0 | all_layers | 900 seconds | 10 | 8 | 50_200 | 100 | 5320 |
| 1  | all_layers | 900 seconds | 20 | 8 | 50_200 | 200 | 4349 |
| 2  | all_layers | 900 seconds | 30 | 8 | 50_200 | 300 | 485 |
| 3  | all_layers | 900 seconds | 40 | 8 | 50_200 | 400 | 7 |
| 4 | all_layers | 300 seconds | 10 | 4 | 100_500 | 229 | 34 |
| 5 | all_layers | 1800 seconds | 8 | 4 | 100_500 | 229 | 57 |
| 6 | all_layers | 300 seconds | 5 | 4 | 100_500 + 200_500 | 292 | 258 |
| 7  | all_layers | 300 seconds | 5 | 4 | 100_1000 | 245 | 221 |
| 8  | all_layers | 3600 seconds | 5 | 4 | 100_1000 | 245 | 330 |
| 9  | all_layers, no application layer | 3600 seconds | 5 | 4 | 100_1000 | 245 | 748 |

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
