import torch
from torch import nn
from .utils import auto_pad
from ._cbam import ChannelAttention, SpatialAttention, CBAM

__all__ = [
	'Conv',
	'WidthBlock',
	'ChannelAttention',
	'SpatialAttention',
	'CBAM',
]


class Conv(nn.Module):
	"""Standard convolution with args(ch_in, ch_out, kernel, stride, padding, groups, dilation, activation)."""
	
	default_act = nn.SiLU()  # default activation
	
	def __init__(self, c1, c2, k=1, s=1, p=None, g=1, d=1, act=True):
		"""Initialize Conv layer with given arguments including activation."""
		super().__init__()
		self.conv = nn.Conv2d(c1, c2, k, s, auto_pad(k, p, d), groups=g, dilation=d, bias=False)
		self.bn = nn.BatchNorm2d(c2)
		self.act = self.default_act if act is True else act if isinstance(act, nn.Module) else nn.Identity()
	
	def forward(self, x):
		"""Apply convolution, batch normalization and activation to input tensor."""
		return self.act(self.bn(self.conv(x)))
	
	def forward_fuse(self, x):
		"""Perform transposed convolution of 2D data."""
		return self.act(self.conv(x))


class WidthBlock(nn.Module):
	
	def __init__(self, c1, c2, kernel_sizes=(3, 5, 7), shortcut=True):
		super().__init__()
		self.convs = nn.ModuleList(
			[Conv(c1, c2, k) for k in kernel_sizes]
		)
		self.final_conv = nn.Conv2d(len(kernel_sizes) * c2, c2, kernel_size=1)
		self.add = shortcut and c1 == c2
	
	def forward(self, x: torch.Tensor):
		y = torch.concatenate([conv(x) for conv in self.convs], dim=1)
		return x + self.final_conv(y) if self.add else self.final_conv(y)
