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
	"""An error raised when an invalid syntax has been encountered.
	"""
	def __init__( self , token , expected=None , eof=False ):
		"""token  :  is the token that invoked the error
		expected  :  is a the string message informing about what the parser expected ( default None )
		eof  :  makes the error becomes a EOF error ( default None )
		"""
		self.token = token;
		self.expected = expected;
		self.eof = False;
	
	def __str__( self ):
		if self.eof:
			return "Parsing error: reached EOF before expected!";
		s = "Parsing error at %d:%d, got token %s "%( self.token.line , self.token.pos , str(self.token) );
		if self.expected != None:
			s += ", expected %s"%( self.expected );
		return s;

class Parser(object):
	"""A parser that will take a list of tokens and returns a AST
	( though this is not forced, any value can be returned. )
	"""
	def __init__( self ):
		self.tokens = [];
		self.index = 0;
		self.channel = 1;
		self.hidden = False;
	
	def cur( self ):
		"""Returns the current token.
		"""
		return self.tokens[self.index]
		
	def lookahead( self , channel=None , hidden=None ):
		"""Returns the next token without moving to it.
		channel  :  the specified channel to handle tokens in ( default self.channel )
		hidden  :  should read hidden tokens ( default self.hidden )
		"""
		channel = channel or self.channel;
		hidden = hidden or self.hidden;
		i = self.index+1;
		if i >= len( self.tokens ):
			raise ParserError( None , None , True ); #Raise a EOF exception
		while self.tokens[i].channel != channel or self.tokens[i].hidden != hidden:
			i += 1;
			if i >= len( self.tokens ):
				raise ParserError( None , None , True ); #Raise a EOF exception
		return self.tokens[i];
	
	def matches( self , ttype , channel=None , hidden=None  ):
		"""Returns if the current token matches the specified type
		ttype  :  the type of the token to check for
		channel  :  the specified channel to handle tokens in ( default self.channel )
		hidden  :  should read hidden tokens ( default self.hidden )
		"""
		channel = channel or self.channel;
		hidden = hidden or self.hidden;
		c = self.cur();
		return c.type == ttype and c.channel == channel and c.hidden == hidden;
		
	def lookaheadmatches( self , ttype , channel=None , hidden=None ):
		"""The same as matches( lookahead(  ) )
		ttype  :  the type of the token to check for
		channel  :  the specified channel to handle tokens in ( default self.channel )
		hidden  :  should read hidden tokens ( default self.hidden )
		"""
		channel = channel or self.channel;
		hidden = hidden or self.hidden;
		return self.lookahead( channel , hidden ).type == ttype;
	
	def hasNext( self , channel=None , hidden=None ):
		"""Returns if there is another token to be read.
		channel  :  the specified channel to handle tokens in ( default self.channel )
		hidden  :  should read hidden tokens ( default self.hidden )
		"""
		channel = channel or self.channel;
		hidden = hidden or self.hidden;
		i = self.index+1;
		if i >= len( self.tokens ):
			return False;
		while self.tokens[i].channel != channel or self.tokens[i].hidden != hidden:
			i += 1;
			if i >= len( self.tokens ):
				return False;
		return True;
	
	def next( self , channel=None , hidden=None ):
		"""Returns current token, and moves to the next token.
		channel  :  the specified channel to handle tokens in ( default self.channel )
		hidden  :  should read hidden tokens ( default self.hidden )
		"""
		channel = channel or self.channel;
		hidden = hidden or self.hidden;
		r = self.tokens[ self.index ]
		i = self.index+1;
		if i >= len( self.tokens ):
			raise ParserError( None , None , True ); #Raise a EOF exception
		while self.tokens[i].channel != channel or self.tokens[i].hidden != hidden:
			i += 1;
			if i >= len( self.tokens ):
				raise ParserError( None , None , True ); #Raise a EOF exception
		self.index = i;
		return r;
	
	# DO NOTE:
	# This method does not apply the given channel and hidden parameters
	# to the next() call, so set the parser variables for that instead
	def nextif( self , ttype , channel=None , hidden=None ):
		"""If the type of the current token matches the specified type, calls next(  )
		ttype  :  the type of the token to check for
		channel  :  the specified channel to handle tokens in ( default self.channel )
		hidden  :  should read hidden tokens ( default self.hidden )
		"""
		channel = channel or self.channel;
		hidden = hidden or self.hidden;
		r = False;
		if self.matches( ttype , channel , hidden ):
			r = self.cur();
			self.next();
		return r;
	
	def expect( self , ttype , channel=None , hidden=None ):
		"""Returns current token if the specified type matches, and calls next(  ) else raises a ParsingError
		ttype  :  the type of the token to check for
		channel  :  the specified channel to handle tokens in ( default self.channel )
		hidden  :  should read hidden tokens ( default self.hidden )
		"""
		channel = channel or self.channel;
		hidden = hidden or self.hidden;
		n = self.nextif( ttype , channel , hidden )
		if not n:
			raise ParserError( self.cur() , ttype );
		else:
			return n;
	
	def parse( self , tokens ):
		"""Parses a list of tokens and returns a AST ( not required though, could return any value )
		This method should be overridden and called from the child class.
		tokens  :  the list of tokens to read from
		"""
		self.tokens = tokens;
		self.index = 0;
	
