# -*- coding: utf-8 -*-
# @Time    : 2023/8/1 11:47
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Schema.py
from typing import List

from ultipa.structs import DBType
from ultipa.structs.Property import Property
from ultipa.structs.BaseModel import BaseModel
from ultipa.types import types

class SchemaPair:
	def __init__(self,fromSchema:str='',toSchema:str='',count:int=None):
		self.fromSchema = fromSchema
		self.toSchema = toSchema
		self.count = count

class Schema(BaseModel):
	'''
	    Data class for schema.
	'''

	def __init__(self, name: str, dbType: DBType,id:int = None,  description: str = None,type:str = '',
				 properties: List[Property] = None,
				 total: int = 0,
				 pair:SchemaPair = None):
		self.id = id
		self.description = description
		self.properties = properties
		self.name = name
		self.total = total
		self.type = type
		self.DBType = dbType
		self.pair = pair


	def getProperty(self, name: str):
		find = list(filter(lambda x: x.get('name') == name, self.properties))
		if find:
			return find[0]
		return None

