# Federated Training in LAN
This is a project for federated training in LAN environment.

```bash
├─Client_1
│  │  Client_1.py
│  │  ModelTrain.py
│  │  SocketCommunicate.py
│  │
│  ├─Data
│  │  │  model_architecture.json
│  │  │
│  │  └─Weight
│  │      │  model_weight.npy
│  │      │
│  │      └─Local
│  │              0.npy
│  │              ......
│  │              9.npy
│  │              Client_0_0.npy
│  │              ......
│  │              Client_1_9.npy
│  │
│  ├─Dataset
│  │  ├─0
│  │  │      train_data.npy
│  │  │      train_label.npy
│  │  │      ......
│  │  └─9
│  │          train_data.npy
│  │          train_label.npy
│  │
│  └─__pycache__
│          ModelTrain.cpython-39.pyc
│          SocketCommunicate.cpython-39.pyc
│
├─Client_2
│  │  Client_2.py
│  │  ModelTrain.py
│  │  SocketCommunicate.py
│  │
│  ├─Data
│  │  │  model_architecture.json
│  │  │
│  │  └─Weight
│  │      │  model_weight.npy
│  │      │
│  │      └─Local
│  │              0.npy
│  │              ......
│  │
│  ├─Dataset
│  │  ├─0
│  │  │      train_data.npy
│  │  │      train_label.npy
│  │  │      ......

│
└─Server
    │  create_model.py
    │  Server.py
    │
    └─Data
        │  model_weight.npy
        │
        ├─OriginFile
        │      model_architecture.json
        │      model_weight.npy
        │
        └─WeightFromClient
            ├─0
            │      0.npy
            │      Client_0_0.npy
            │      Client_1_0.npy
            │ ......
            │
            └─9
                    9.npy
                    Client_0_9.npy
                    Client_1_9.npy
```
