# Copyright (C) 2013  Marco Aslak Persson
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#


from IceLeaf import *

class ASTObject(object):
	"""An abstract syntax tree object, which has an identifying type,
	and then a dynamic set of variables. You can get the underlying
	dictionary with ._data
	"""
	def __init__( self , type , **data ):
		"""type  :  the type of the AST
		**data  :  the starting data for the AST
		"""
		self.__dict__["type"] = type;
		self.__dict__["data"] = data;
	
	def haskey( self , key ):
		return self.__dict__["data"].has_key( key );
	
	def __getattr__( self , name ):
		if name == "type":
			return self.__dict__["type"];
		elif name == "_data":
			return self.__dict__["data"];
		else:
			return self.__dict__["data"][name];
	
	def __setattr__( self , name , value ):
		if name != "type" and name != "_data":
			self.__dict__["data"][name] = value;
		elif name == "_data":
			self.__dict__["data"] = value;
		elif name == "type":
			self.__dict__["type"] = value;
			
	
	def __str__( self ):
		dstr = "{ ";
		d = self._data;
		for k in d.keys():
			if type( d[k] ) == list:
				dd = "[ ";
				for item in d[k]:
					dd += "%s , "%(str(item));
				dd += "]"
			else:
				dd = str(d[k]);
			dstr += "%s: %s , "%( k , dd )
		dstr += "}";
		return "ASTObject.%s%s"%( self.type , dstr );
