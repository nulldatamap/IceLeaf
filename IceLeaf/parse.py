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

class ParserError(Exception):
	def __init__( self , token , expected=None , eof=False ):
		self.token = token;
		self.expected = expected;
		self.eof = False;
	
	def __str__( self ):
		if self.eof:
			return "Parsing error: reached EOF before expected!";
		s = "Parsing error at %d:%d, got token %s "%( self.token.line , self.token.pos , str(self.token) );
		if self.expected != None:
			s += ", expected '%s'"%( self.expected );
		return s;

class Parser(object):
	def __init__( self ):
		self.tokens = [];
		self.index = 0;
	
	def cur( self ):
		return self.tokens[self.index]
		
	def lookahead( self ):
		if self.index+1 >= len( self.tokens ):
			raise ParseError( None , None , True ); #Raise a EOF exception
		return self.tokens[self.index+1];
	
	def matches( self , ttype ):
		return self.cur().type == ttype;
		
	def lookaheadmatches( self , ttype ):
		return self.lookahead().type == ttype;
	
	def next( self ):
		r = self.tokens[ self.index ]
		self.index += 1;
		if self.index >= len( self.tokens ):
			raise ParseError( None , None , True ); #Raise a EOF exception
		return r;
	
	def nextif( self , ttype ):
		r = False;
		if self.matches( ttype ):
			r = self.cur();
			self.next();
		return r;
	
	def expect( self , ttype ):
		n = self.nextif( ttype )
		if not n:
			raise ParserError( self.cur() , ttype );
		else:
			return n;
	
	def parse( self , tokens ):
		return {};