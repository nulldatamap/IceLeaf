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
		self.channel = 1;
		self.hidden = False;
	
	def cur( self ):
		return self.tokens[self.index]
		
	def lookahead( self , channel=self.channel , hidden=self.hidden ):
		i = self.index+1;
		if i >= len( self.tokens ):
			raise ParseError( None , None , True ); #Raise a EOF exception
		while self.tokens[i].channel != channel or self.tokens[i].hidden != hidden:
			i += 1;
			if i >= len( self.tokens ):
				raise ParseError( None , None , True ); #Raise a EOF exception
		return self.tokens[i];
	
	def matches( self , ttype , channel=self.channel , hidden=self.hidden  ):
		c = self.cur();
		return c.type == ttype and c.channel == channel and c.hidden == hidden;
		
	def lookaheadmatches( self , ttype , channel=self.channel , hidden=self.hidden ):
		return self.lookahead( channel , hidden ).type == ttype;
	
	def next( self , channel=self.channel , hidden=self.hidden ):
		r = self.tokens[ self.index ]
		i = self.index+1;
		if i >= len( self.tokens ):
			raise ParseError( None , None , True ); #Raise a EOF exception
		while self.tokens[i].channel != channel or self.tokens[i].hidden != hidden:
			i += 1;
			if i >= len( self.tokens ):
				raise ParseError( None , None , True ); #Raise a EOF exception
		self.index = i;
		return r;
	
	# DO NOTE:
	# This method does not apply the given channel and hidden parameters
	# to the next() call, so set the parser variables for that instead
	def nextif( self , ttype , channel=self.channel , hidden=self.hidden ):
		r = False;
		if self.matches( ttype , channel , hidden ):
			r = self.cur();
			self.next();
		return r;
	
	def expect( self , ttype , channel=self.channel , hidden=self.hidden ):
		n = self.nextif( ttype , channel , hidden )
		if not n:
			raise ParserError( self.cur() , ttype );
		else:
			return n;
	
	def parse( self , tokens ):
		return {};