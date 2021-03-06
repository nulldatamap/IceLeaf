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

import re


class Token( object ):
	"""An object representing a terminal symbol containing data
	about it's literal value, source position and channel.
	"""
	def __init__( self , type , data , pos , line ):
		"""type  :  the type of the token ( Usually a LexerRule )
		data  :  the data of the token
		pos  :  the line position of the token
		line  :  the line number of the token
		"""
		if type == "EOF":
			self.type = "EOF";
			self.channel = 1;
			self.hidden = False;
		else:
			self.type = type.type;
			self.channel = type.channel;
			self.hidden = type.hidden;
		self.data = data;
		self.pos = pos;
		self.line = line;

	def __str__( self ):
		s = "Token.%s{"%( self.type );
		if self.hidden:
			s += "hidden"
		s += " '%s' at %d:%d"%( self.data.replace("\n","\\n") , self.line , self.pos );
		if self.channel != 1:
			s += " in channel %d"%( self.channel );
		s += " }";
		return s;

	def __repr__( self ):
		return str( self );

class LexerError( Exception ):
	"""An object representing a failure in the lexing process.
	"""
	def __init__( self , pos , line ):
		"""pos  :  the line position of the lexing error
		line  :  the line number of the lexing error
		"""
		self.pos = pos;
		self.line = line;

	def __str__( self ):
		return "Lexing error at %d:%d"%(self.line,self.pos)

class TokenType( object ):
	"""A declaration of a token type without a definition.
	This class is only used internally for the EOF token.
	"""
	def __init__( self , type , channel = 1 , hidden = False ):
		"""type  :  the name of the type
		channel  :  the channel the token will be in ( default 1 )
		hidden  :  the token's visibility ( default True )
		"""
		self.type = type;
		self.channel = channel;
		self.hidden = hidden;

class LexerRule( TokenType ):
	"""The lexer rule defines a pattern for a token, and what
	type of token this will yield. A channel and visibility
	can also be specified.
	"""
	def __init__( self ,typename , regex , channel = 1 , hidden = False ):
		"""typename  :  the name of the token the rule will produce
		regex  :  the regex string representing the pattern
		channel  :  the channel the token will be in ( default 1 )
		hidden  :  the token's visibility ( default True )
		"""
		TokenType.__init__( self, typename , channel , hidden );
		self.regex = re.compile( regex );

class StateError( Exception ):
	"""A state error is manually thrown type of error
	that should be thrown in case of an unrecoverable
	error inside of a state function.
	"""
	def __init__( self , state , rsn , pos , line ):
		"""state  :  the name of the state where the occurred
		rsn  :  the reason behind the error
		pos  :  the line position of where the error occurred
		line  :  the line number of where the error occurred
		"""
		self.state = state;
		self.reason = rsn;
		self.pos = pos;
		self.line = line;

	def __str__( self ):
		return "State error \"%s\", in state %s at %d:%d"%(self.reason,self.state,self.line,self.pos);

class LexerState( object ):
	"""A lexer state is a function triggered by
	a regex pattern. It should be used for patterns
	that can't be defined by normal regex or needs
	special lexing conditions.
	"""
	def __init__( self , state , regex , statefunc ):
		"""state  :  the name of the state
		regex  :  the regex string representing the pattern
		statefunc  :  the function that is invoked when the pattern has been mathced
		statefunc( lexer , statename )
		"""
		self.state = state;
		self.regex = re.compile( regex );
		self.func = statefunc;

class Lexer( object ):
	"""The lexer takes a string of source code
	and reads the given rules and returns a
	token list. The token list is what the
	parser will work off.
	"""
	def __init__( self , *rules ):
		"""*rules  :  an unpacked list of lexer rules and states
		"""
		self.source = "";
		self.rules = [];
		self.rulere = "";
		self.state = None;
		self.tokens = [];
		self.index = 0;
		self.pos = 1;
		self.line = 1;
		self.rules = rules;

	def nexttoken( self ):
		"""Returns the next valid token, or None if EOF has been reached.
		It raises a lexing error if no lexer rule mathces.
		"""
		if self.index == len( self.source ):
			return None;
		for i in range( len( self.rules ) ):
			m = self.rules[i].regex.match( self.source[self.index:] )
			if m == None:
				if i == len( self.rules ) - 1:
					print self.source[self.index:]
					raise LexerError( self.pos , self.line );
				continue;
			if isinstance ( self.rules[i] , LexerState ):
				self.state = self.rules[i];
				return Token( LexerRule("IGNORE",""), 0 , 0 , 0 );
			if self.rules[i].type == "NEWLINE":
				self.line+=1;
				self.pos = 1;
				self.index += 1;
			else:
				c = m.group(0).count("\n");
				self.line += c
				if c == 0:
					self.pos += len( m.group(0) );
				else:
					self.pos = len( m.group(0).split("\n")[-1] )
				self.index += len( m.group(0) )
			return Token( self.rules[i] , m.group(0) , self.pos - len( m.group(0) ) , self.line );


	def lex( self , source ):
		"""Lexes the source string into a list of tokens.
		The last token will always be a EOF token.
		Lexer errors from nexttoken will bubble up.
		source  :  the source string to lex
		"""
		self.index = 0;
		self.pos = 1;
		self.line = 1;
		self.state = None;
		self.source = source;
		self.tokens = []
		s = self.nexttoken();
		while s != None:
			if s.type != "IGNORE":
				self.tokens.append( s );
			s = self.nexttoken();
			if self.state != None:
				self.state.func( self , self.state.state );
				self.state = None;
		self.tokens.append( Token( "EOF","",self.pos,self.line ) );
		i = 0;
		return self.tokens;
