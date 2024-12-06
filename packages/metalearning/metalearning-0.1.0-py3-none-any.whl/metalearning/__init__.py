import torch
import torch.nn as nn
import torch.optim as optim


class MAML:
    def __init__(self, model, meta_lr, task_lr, inner_steps=1):
        """
        Initialize the MAML class.
        
        Parameters:
        - model: The neural network model to be trained.
        - meta_lr: The learning rate for the meta-optimizer.
        - task_lr: The learning rate for the inner-loop optimizer.
        - inner_steps: Number of gradient descent steps in the inner loop.
        """
        self.model = model
        self.meta_optimizer = optim.Adam(self.model.parameters(), lr=meta_lr)
        self.task_lr = task_lr
        self.inner_steps = inner_steps

    def train_step(self, tasks, device='cpu'):
        """
        Perform one meta-training step.
        
        Parameters:
        - tasks: A list of tasks, where each task is a tuple (support_set, query_set).
        - device: Device to run the computations on (e.g., 'cpu' or 'cuda').
        """
        meta_loss = 0.0
        for support_set, query_set in tasks:
            # Inner loop: Adapt the model to the support set
            fast_weights = self._inner_loop(support_set, device)
            
            # Outer loop: Evaluate the adapted model on the query set
            query_inputs, query_labels = query_set
            query_inputs, query_labels = query_inputs.to(device), query_labels.to(device)
            query_outputs = self.model(query_inputs, fast_weights)
            query_loss = nn.CrossEntropyLoss()(query_outputs, query_labels)
            meta_loss += query_loss

        # Meta-update: Update the model parameters based on the meta-loss
        meta_loss /= len(tasks)
        self.meta_optimizer.zero_grad()
        meta_loss.backward()
        self.meta_optimizer.step()

    def _inner_loop(self, support_set, device):
        """
        Perform the inner loop adaptation.
        
        Parameters:
        - support_set: The support set for the current task.
        - device: Device to run the computations on (e.g., 'cpu' or 'cuda').
        
        Returns:
        - fast_weights: Updated weights after inner loop adaptation.
        """
        support_inputs, support_labels = support_set
        support_inputs, support_labels = support_inputs.to(device), support_labels.to(device)
        
        fast_weights = {k: v.clone() for k, v in self.model.named_parameters()}
        
        for _ in range(self.inner_steps):
            outputs = self.model(support_inputs, fast_weights)
            loss = nn.CrossEntropyLoss()(outputs, support_labels)
            grads = torch.autograd.grad(loss, fast_weights.values(), create_graph=True)
            fast_weights = {k: v - self.task_lr * grad for k, v, grad in zip(fast_weights.keys(), fast_weights.values(), grads)}
        
        return fast_weights

    def evaluate(self, tasks, device='cpu'):
        """
        Evaluate the model on a list of tasks.
        
        Parameters:
        - tasks: A list of tasks, where each task is a tuple (support_set, query_set).
        - device: Device to run the computations on (e.g., 'cpu' or 'cuda').
        
        Returns:
        - accuracy: Average accuracy across the tasks.
        """
        total_correct = 0
        total_samples = 0
        for support_set, query_set in tasks:
            fast_weights = self._inner_loop(support_set, device)
            
            query_inputs, query_labels = query_set
            query_inputs, query_labels = query_inputs.to(device), query_labels.to(device)
            query_outputs = self.model(query_inputs, fast_weights)
            _, predicted = torch.max(query_outputs, 1)
            correct = (predicted == query_labels).sum().item()
            total_correct += correct
            total_samples += query_labels.size(0)
        
        accuracy = total_correct / total_samples
        return accuracy
