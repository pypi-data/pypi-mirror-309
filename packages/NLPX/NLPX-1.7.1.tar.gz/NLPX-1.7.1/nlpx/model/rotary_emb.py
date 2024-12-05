import torch
from typing import Tuple

__all__ = [
	'precompute_freqs_cis',
	'reshape_for_broadcast',
	'apply_rotary_emb',
	'apply_rotary_emb_self'
]


def precompute_freqs_cis(dim: int, end: int, theta: float = 10000.0):
	freqs = 1.0 / (theta ** (torch.arange(0, dim, 2)[: (dim // 2)].float() / dim))
	t = torch.arange(end, device=freqs.device, dtype=torch.float32)
	freqs = torch.outer(t, freqs)
	freqs_cis = torch.polar(torch.ones_like(freqs), freqs)  # complex64
	return freqs_cis


def reshape_for_broadcast(freqs_cis: torch.Tensor, x: torch.Tensor):
	ndim = x.ndim
	assert 0 <= 1 < ndim
	assert freqs_cis.shape == (x.shape[1], x.shape[-1])
	shape = [d if i == 1 or i == ndim - 1 else 1 for i, d in enumerate(x.shape)]
	return freqs_cis.view(*shape)


def apply_rotary_emb(
		xq: torch.Tensor,
		xk: torch.Tensor,
		freqs_cis: torch.Tensor,
) -> Tuple[torch.Tensor, torch.Tensor]:
	xq_ = torch.view_as_complex(xq.float().reshape(*xq.shape[:-1], -1, 2))
	xk_ = torch.view_as_complex(xk.float().reshape(*xk.shape[:-1], -1, 2))
	freqs_cis = reshape_for_broadcast(freqs_cis, xq_)
	xq_out = torch.view_as_real(xq_ * freqs_cis).flatten(-2)
	xk_out = torch.view_as_real(xk_ * freqs_cis).flatten(-2)
	return xq_out.type_as(xq), xk_out.type_as(xk)


def apply_rotary_emb_self(inputs: torch.Tensor, freqs_cis: torch.Tensor) -> torch.Tensor:
	x_ = torch.view_as_complex(inputs.float().reshape(*inputs.shape[:-1], -1, 2))
	freqs_cis = reshape_for_broadcast(freqs_cis, x_)
	xq_out = torch.view_as_real(x_ * freqs_cis).flatten(-2)
	return xq_out.type_as(inputs)


if __name__ == '__main__':
	batch_size = 4
	seq_length = 10
	word_dim = 16
	X = torch.randn(batch_size, seq_length, word_dim)
	
	# freqs_cis = precompute_freqs_cis(word_dim, seq_length * 2)
	# print('freqs_cis1', freqs_cis.shape)
	# freqs_cis = freqs_cis[0: 0 + seq_length]
	# print('freqs_cis2', freqs_cis.shape)
	#
	# xq, xk = apply_rotary_emb(X, X, freqs_cis=freqs_cis)
	# print('xq', xq.shape, 'xk', xk.shape,)
	# print(xq[:3])
	# print(xk[:3])
	
	# rotary_emb = RotaryEmbedding(word_dim)
	# print('rotary_emb', rotary_emb(X))

