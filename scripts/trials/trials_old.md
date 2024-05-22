### notes 

Models: 100, 200, 300, 400
Min number of nodes: 8
Min support: 10%

> {8,10%} combination with all layers x 4 - ok
> {8,10%} each layer x 3
> {8,10%} per pair of layers x 3

### all_layers

trial_0
all_layers
900_s
Selected values: [10, 8]
100 models 50_200

trial_1 
all_layers
900_s
Selected values: [20, 8]
200 models 50_200

trial_2 
all_layers
900_s
Selected values: [30, 8]
300 models 50_200

trial_3 
all_layers
900_s
Selected values: [40, 8]
400 models 50_200

trial_4
all_layers
300_s
Selected values: [10, 4]
229 models 100_500

trial_5
all_layers
1800_s
Selected values: [8, 4]
229 models 100_500

trial_6
all_layers
300_s
Selected values: [5, 4]
292 models 100_500 + 200_500

trial_7 
all_layers
300_s
Selected values: [5, 4]
245 models 100_1000

trial_8 
all_layers
3600_s
Selected values: [5, 4]
245 models 100_1000

trial_9 
all_layers, no application layer
3600_s
Selected values: [5, 4]
245 models 100_1000

### single_layers

trial_0
application_layer
900_s
Selected values: [20, 8]
300 models 50_200

trial_1
business_layer
900_s
Selected values: [20, 8]
300 models 50_200

<Implementation & Mitigation> (no patterns with support "10" and nodes "4", over 300)

trial_2
motivation_layer
900_s
Selected values: [10, 4]
300 models 50_200

<Other> (crashes most of the times, with 200 models, support 20 and 8 nodes. It found 6 patterns only with 100 models, 10 support and 4 nodes)

<Physical> (no patterns with support "8" and nodes "4", over 300)

trial_3
strategy_layer
900_s
Selected values: [8, 4]
300 models 50_200

trial_4
technology_layer
900_s
Selected values: [8, 4]
300 models 50_200

trial_5
technology_layer
900_s
Selected values: [20, 4]
300 models 50_200

trial_6
motivation_layer
300_s
Selected values: [10, 4]
229 models 100_500

trial_7
motivation_layer
300_s
Selected values: [10, 4]
292 models 100_500 + 200_500

trial_8
business_layer
3600_s
Selected values: [60, 4]
292 models 100_1000

### combined_layers

trial_0_0
business + application
900_s
Selected values: [10, 8]
300 models 50_200

trial_0_1
business + application
900_s
Selected values: [10, 12]
300 models 50_200

trial_0_2
business + strategy
900_s
Selected values: [20, 8]
300 models 50_200

trial_0_3
business + motivation
900_s
Selected values: [10, 8]
300 models 50_200

trial_0
business + application + technology
1800_s
Selected values: [10, 6]
245 models 100_1000
--> crashes after some time (out of memory)

trial_1_0
application + technology
900_s
Selected values: [20, 8]
300 models 50_200

trial_1_1
application + motivation
900_s
Selected values: [20, 8]
300 models 50_200

trial_1_2
application + technology + physical
900_s
Selected values: [20, 8]
300 models 50_200

trial_1_3
application + technology + physical
900_s
Selected values: [10, 8]
300 models 50_200

trial_1
application + technology + other
900_s
Selected values: [8, 6]
245 models 100_1000

trial_2_0
motivation + strategy
900_s
Selected values: [10, 6]
300 models 50_200

trial_3_0
implementation & migration + physical + technology
900_s
Selected values: [10, 8]
300 models 50_200

trial_3_1
implementation & migration + motivation + other + strategy
900_s
Selected values: [10, 8]
300 models 50_200

trial_2
technology + physical + implementation_migration
900_s
Selected values: [8, 6]
245 models 100_1000

trial_3
motivation + strategy + other
900_s
Selected values: [8, 6]
245 models 100_1000
--> only 1 pattern found

trial_4
application + technology + physical
900_s
Selected values: [10, 8]
245 models 100_1000

trial_5
motivation + strategy + other + implementation_migration
900_s
Selected values: [8, 8]
245 models 100_1000
--> No patterns found
