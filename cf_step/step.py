# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/step.ipynb (unless otherwise specified).

__all__ = ['Step']

# Cell
import torch
import numpy as np

from tqdm import tqdm
from .networks import SimpleCF

# Cell
class Step:
    """Incremental and batch training of recommender systems."""
    def __init__(self, model, objective, optimizer, conf_func=lambda x: 1):
        self.model = model
        self.objective = objective
        self.optimizer = optimizer
        self.conf_func = conf_func

        # check if the user has provided user and item embeddings
        assert self.model.user_embeddings, 'User embedding matrix could not be found.'
        assert self.model.item_embeddings, 'Item embedding matrix could not be found.'

    @property
    def user_embeddings(self):
        return self.model.user_embeddings

    @property
    def item_embeddings(self):
        return self.model.item_embeddings

    def batch_fit(self, data_loader, epochs=1):
        """Batch fits the recommender system."""
        self.model.train()
        for epoch in range(epochs):
            with tqdm(total=len(data_loader)) as pbar:
                for _, (users, items, ratings, preferences) in enumerate(data_loader):
                    predictions = self.model(users, items)
                    conf = self.conf_func(ratings)
                    loss = (conf * self.objective(predictions, preferences)).mean()
                    loss.backward()
                    self.optimizer.step()
                    self.optimizer.zero_grad()
                    pbar.update(1)

    def step(self, user, item, rating=None, preference=None):
        """Fits the recommender system incrementally."""
        self.model.train()
        prediction = self.model(user, item)
        conf = self.conf_func(rating)
        loss = conf * self.objective(prediction, preference)
        loss.backward()
        self.optimizer.step()
        self.optimizer.zero_grad()

    def predict(self, user, k):
        """Recommends items to a specific user."""
        self.model.eval()
        user_embedding = self.user_embeddings(user)
        item_embeddings = self.item_embeddings.weight
        score = item_embeddings @ user_embedding.transpose(0, 1)
        predictions = score.squeeze().argsort()[-k:]
        return predictions

    def save(self, path):
        """Saves the model parameters to the given path."""
        torch.save(self.model.state_dict(), path)

    def load(self, path):
        """Loads the model parameters from a given path."""
        self.model.load_state_dict(torch.load(path))