import numpy as np
from PIL import Image
from pathlib import Path
import torch
from torch import nn
from torch import optim
from typing import Union, Tuple, Collection
from torch.optim.lr_scheduler import LRScheduler
from torchvision import transforms
from torchvision.datasets import ImageFolder

from model_wrapper.training.utils import acc_predict
from model_wrapper import ModelWrapper, SimpleModelWrapper, ClassModelWrapper, SimpleClassModelWrapper, \
	SplitClassModelWrapper, RegressModelWrapper, SimpleRegressModelWrapper, SplitRegressModelWrapper, log_utils

__all__ = [
	'ModelWrapper',
	'SimpleModelWrapper',
	'ClassModelWrapper',
	'SimpleClassModelWrapper',
	'SplitClassModelWrapper',
	'ImageClassModelWrapper',
	'RegressModelWrapper',
	'SimpleRegressModelWrapper',
	'SplitRegressModelWrapper'
]


class ImageClassModelWrapper(ClassModelWrapper):
	"""
	Examples
	--------
	>>> model_wrapper = ImageClassModelWrapper(model, tokenize_vec, classes=classes)
	>>> model_wrapper.train(train_texts, y_train val_data, collate_fn)
	>>> model_wrapper.predict(test_texts)
	>>> model_wrapper.evaluate(test_texts, y_test)
	"""
	
	test_dir: Path
	
	def __init__(self, model_or_path: Union[nn.Module, str, Path],
	             classes: Collection[str] = None,
	             device: torch.device = None):
		super().__init__(model_or_path, classes, device)
		self.test_dir = None
		self.imgsz = None
		self.transform = None
	
	def train(self, data: Union[str, Path], imgsz: Union[int, tuple, list] = None,
	          transform=None, train_transform=None,
	          epochs=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          lr=0.001, T_max: int = 0,
	          batch_size=64, eval_batch_size=128,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = None,
	          print_per_rounds: int = 1, checkpoint_per_rounds: int = 0, checkpoint_name='model.pt',
	          show_progress=False, eps=1e-5) -> dict:
		if isinstance(data, str):
			data = Path(data)
		
		train_dir = data / 'train'
		test_dir = data / 'test'
		val_dir = data / 'val'
		if not val_dir.exists():
			val_dir = data / 'valid'
		
		assert train_dir.exists()
		
		if transform is None:
			if imgsz:
				transform = transforms.Compose([
					transforms.Resize(imgsz),
					transforms.ToTensor()
				])
			else:
				transform = transforms.Compose([
					transforms.ToTensor()
				])
			if train_transform is None:
				train_transform = transforms.Compose([
					transforms.Resize(imgsz),
					transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
					transforms.RandomAffine(degrees=(-10, 10), translate=(0.1, 0.1), scale=(0.9, 1.1), shear=(-10, 10)),
					transforms.ToTensor()
				])
		
		self.transform = transform
		train_transform = train_transform or transform
		train_set = ImageFolder(train_dir, train_transform)
		self.classes = train_set.classes
		log_utils.info(f"Classes: {self.classes}")
		
		if val_dir.exists():
			val_set = ImageFolder(val_dir, transform)
			result = super().train(train_set, val_set,
			                       epochs=epochs, optimizer=optimizer, scheduler=scheduler, lr=lr,
			                       T_max=T_max, batch_size=batch_size, eval_batch_size=eval_batch_size,
			                       num_workers=num_workers, num_eval_workers=num_eval_workers,
			                       pin_memory=pin_memory, pin_memory_device=pin_memory_device,
			                       persistent_workers=persistent_workers,
			                       early_stopping_rounds=early_stopping_rounds, print_per_rounds=print_per_rounds,
			                       checkpoint_per_rounds=checkpoint_per_rounds, checkpoint_name=checkpoint_name,
			                       show_progress=show_progress, eps=eps)
			if test_dir.exists():
				self.test_dir = test_dir
				test_set = ImageFolder(val_dir, transform)
				print(f'Test 准确率: {super().evaluate(test_set):.2%}')
			return result
		elif test_dir.exists():
			self.test_dir = test_dir
			test_set = ImageFolder(test_dir, transform)
			return super().train(train_set, test_set,
			                     epochs=epochs, optimizer=optimizer, scheduler=scheduler, lr=lr,
			                     T_max=T_max, batch_size=batch_size, eval_batch_size=eval_batch_size,
			                     num_workers=num_workers, num_eval_workers=num_eval_workers,
			                     pin_memory=pin_memory, pin_memory_device=pin_memory_device,
			                     persistent_workers=persistent_workers,
			                     early_stopping_rounds=early_stopping_rounds, print_per_rounds=print_per_rounds,
			                     checkpoint_per_rounds=checkpoint_per_rounds, checkpoint_name=checkpoint_name,
			                     show_progress=show_progress, eps=eps)
		return super().train(train_set,
		                     epochs=epochs, optimizer=optimizer, scheduler=scheduler, lr=lr,
		                     T_max=T_max, batch_size=batch_size, num_workers=num_workers, pin_memory=pin_memory,
		                     pin_memory_device=pin_memory_device, persistent_workers=persistent_workers,
		                     early_stopping_rounds=early_stopping_rounds, print_per_rounds=print_per_rounds,
		                     checkpoint_per_rounds=checkpoint_per_rounds, checkpoint_name=checkpoint_name,
		                     show_progress=show_progress, eps=eps)
	
	def predict(self, source: Union[str, Path, Image.Image, list, tuple, np.ndarray, torch.Tensor],
	            imgsz: Union[int, tuple, list] = None) -> np.ndarray:
		"""
		:param source:
		:param imgsz: 图片大小
		"""
		logits = self.logits(source, imgsz)
		return acc_predict(logits)
	
	def predict_classes(self, source: Union[str, Path, Image.Image, list, tuple, np.ndarray, torch.Tensor],
	                    imgsz: Union[int, tuple, list] = None) -> list:
		"""
		:param source:
		:param imgsz: 图片大小
		"""
		pred = self.predict(source, imgsz)
		return self._predict_classes(pred.ravel())
	
	def predict_proba(self, source: Union[str, Path, Image.Image, list, tuple, np.ndarray, torch.Tensor],
	                  imgsz: Union[int, tuple, list] = None) -> Tuple[np.ndarray, np.ndarray]:
		"""
		:param source:
		:param imgsz: 图片大小
		"""
		logits = self.logits(source, imgsz)
		return self._proba(logits)
	
	def predict_classes_proba(self, source: Union[str, Path, Image.Image, list, tuple, np.ndarray, torch.Tensor],
	                          imgsz: Union[int, tuple, list] = None) -> Tuple[list, np.ndarray]:
		"""
		:param source:
		:param imgsz: 图片大小
		"""
		indices, values = self.predict_proba(source, imgsz)
		return self._predict_classes(indices.ravel()), values
	
	def logits(self, source: Union[str, Path, Image.Image, list, tuple, np.ndarray, torch.Tensor],
	           imgsz: Union[int, tuple, list] = None) -> torch.Tensor:
		imgsz = imgsz or self.imgsz
		if imgsz:
			transform = transforms.Compose([
				transforms.Resize(imgsz),
				transforms.ToTensor()
			])
		else:
			if self.transform:
				transform = self.transform
			else:
				raise ValueError("Expected 'imgsz', but None")
		
		if isinstance(source, str):
			source = Path(source)
		if isinstance(source, Path):
			if source.is_file():
				source = Image.open(source)
			elif source.is_dir():
				source = (img for img in source.rglob('*') if img.suffix in ('.png', '.jpg', 'jpeg') and img.is_file())
				source = [transform(Image.open(s)).unsqueeze(0) for s in source]
				source = torch.cat(source, dim=0)
		if isinstance(source, Image.Image):
			source = transform(source)
			source = source.unsqueeze(0)
		
		return super().logits(source)
	
	def evaluate(self, data: Union[str, Path] = None,
	             imgsz: Union[int, tuple, list] = None,
	             transform=None,
	             batch_size: int = 64,
	             num_workers: int = 0) -> float:
		""" return accuracy """
		data = data or self.test_dir
		if transform is None:
			if imgsz:
				transform = transforms.Compose([
					transforms.Resize(imgsz),
					transforms.ToTensor()
				])
			else:
				transform = self.transform or transforms.Compose([
					transforms.ToTensor()
				])
		dataset = ImageFolder(data, transform)
		return super().evaluate(dataset, batch_size, num_workers, None)
