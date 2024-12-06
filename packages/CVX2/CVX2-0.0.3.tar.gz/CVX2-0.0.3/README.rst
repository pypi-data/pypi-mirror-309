Usage Sample
''''''''''''

.. code:: python

        import torch
        from torch import nn
        from cvx2 import WidthBlock

        model = nn.Sequential(
            WidthBlock(c1=1, c2=32),
            nn.MaxPool2d(kernel_size=2, stride=2),
            WidthBlock(c1=32, c2=64),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Flatten(),
            nn.Linear(in_features=64*49, out_features=1024),
            nn.Dropout(0.2),
            nn.SiLU(inplace=True),
            nn.Linear(in_features=1024, out_features=2),
        )

        img = torch.randn(1, 1, 28, 28)
        print(model(img).shape)
