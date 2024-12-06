import torch
import torch.nn as nn
import torch.nn.functional as F

from . import MAML


class ExampleNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ExampleNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x, params=None):
        if params is None:
            params = {k: v for k, v in self.named_parameters()}
        
        x = F.relu(F.linear(x, params['fc1.weight'], params['fc1.bias']))
        x = F.linear(x, params['fc2.weight'], params['fc2.bias'])
        return x


def maml_example():
    # Hyperparameters
    input_size = 10
    hidden_size = 20
    output_size = 5
    meta_lr = 0.001
    task_lr = 0.1
    inner_steps = 1
    num_tasks = 10
    num_epochs = 100

    # Create a simple model
    model = ExampleNetwork(input_size, hidden_size, output_size)

    # Create a MAML instance
    maml = MAML(model, meta_lr, task_lr, inner_steps)

    # Generate some dummy tasks
    tasks = []
    for _ in range(num_tasks):
        support_set = (torch.randn(5, input_size), torch.randint(0, output_size, (5,)))
        query_set = (torch.randn(5, input_size), torch.randint(0, output_size, (5,)))
        tasks.append((support_set, query_set))

    # Train the model
    for epoch in range(num_epochs):
        maml.train_step(tasks)
        if epoch % 10 == 0:
            accuracy = maml.evaluate(tasks)
            print(f"Epoch {epoch}, Accuracy: {accuracy:.4f}")

    # Final evaluation
    final_accuracy = maml.evaluate(tasks)
    print(f"Final Accuracy: {final_accuracy:.4f}")
