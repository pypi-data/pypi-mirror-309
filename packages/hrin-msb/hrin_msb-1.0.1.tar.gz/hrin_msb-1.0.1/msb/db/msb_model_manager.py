from django.db import models
from msb.cipher import Cipher

from .constants import (COLUMN_NAME_DELETED)


class MsbModelManager(models.Manager):
	_default_filters = {}
	_exclude_filters = {}

	def _get_filtered_queryset(self, **filters):
		_query_set = super(MsbModelManager, self).get_queryset()
		query_filters = {k: v for k, v in filters.items() if hasattr(self.model, k)}
		return _query_set.filter(**query_filters)

	def retrieve(self, *args, **kwargs):
		return super(MsbModelManager, self).get(*args, **kwargs)

	def get(self, *args, **kwargs):
		pk = kwargs.get('pk')
		if pk is not None and isinstance(pk, str):
			kwargs.update(dict(pk=int(Cipher.decipher(pk))))
		return self.retrieve(*args, **kwargs)

	@property
	def deleted(self):
		return self._get_filtered_queryset(**{COLUMN_NAME_DELETED: True})

	@property
	def from_all(self):
		return super(MsbModelManager, self).get_queryset()

	def get_queryset(self):
		return self._get_filtered_queryset(
			**{COLUMN_NAME_DELETED: False, **self._default_filters}
		).exclude(**self._exclude_filters)
