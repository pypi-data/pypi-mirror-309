from typing import Collection, List, Tuple
import numpy as np
import torch


def is_float(x) -> bool:
	if isinstance(x, (Collection, np.ndarray)):
		return is_float(x[0])
	return isinstance(x, (float, np.float_, np.float16, np.float16, np.float32, np.float64, np.float128, np.single, np.double))


def convert_to_tensor(x, dim_start=1) -> torch.Tensor:
	if 1 == dim_start:
		return torch.tensor(x, dtype=torch.float) if is_float(x[0]) else torch.tensor(x, dtype=torch.long)
	return torch.tensor(x, dtype=torch.float) if is_float(x[0][0]) else torch.tensor(x, dtype=torch.long)


def convert_data(X, y) -> Tuple[torch.Tensor, torch.Tensor]:
	if isinstance(X, (List, np.ndarray)):
		X = convert_to_tensor(X, 2)
	if isinstance(y, (List, np.ndarray)):
		y = convert_to_tensor(y)
	return X, y


def convert_data_r2(X, y) -> Tuple[torch.Tensor, torch.FloatTensor]:
	if isinstance(X, (List, np.ndarray)):
		X = convert_to_tensor(X, 2)
	if isinstance(y, (List, np.ndarray)):
		y = torch.tensor(y, dtype=torch.float)
	return X, y


def cal_count(y) -> int:
	shape = y.shape
	return shape[0] if len(shape) == 1 else shape[0] * shape[1]


def acc_predict(logits: torch.Tensor) -> np.ndarray:
	logits = logits.detach().numpy()
	shape_len = len(logits.shape)
	if shape_len == 1:
		return np.where(logits >= 0.5, 1, 0).astype(np.int64)
	elif shape_len == 2 and logits.shape[1] == 1:
		return np.where(logits.ravel() >= 0.5, 1, 0).astype(np.int64)
	else:
		return logits.argmax(-1)
	
	
def cal_correct(logits: torch.Tensor, y: torch.Tensor) -> np.int64:
	return (acc_predict(logits) == y.numpy()).sum()
