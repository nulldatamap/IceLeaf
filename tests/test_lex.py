from IceLeaf import *

# Test if the lexer works like it should do
# Also this might be good code to learn by example.


# LexerRule( "TOKEN_TYPE_NAME" , "my(Reg)+ex*" );


# NEWLINE is a special token that is vital to make linenumbers work
# The number argument given is the channel that the token will be in ( default is 1 )
# And the visibility of the token ( default is True )
lNewline = LexerRule( "NEWLINE" , "\n" , 0 , False );

# IGNORE is another special token that when found, is instantly discarded.
lIgnore = LexerRule( "IGNORE" , "[\t \r]" );

lString = LexerRule( "STRING" , '"((\\\\")|[^"])*[^\\\\]"' );
lIdent = LexerRule( "IDENT" , "[a-zA-Z_][a-zA-Z_0-9]*" );
lHex = LexerRule( "HEX" , "0x[a-fA-F0-9]+" );
lFloat = LexerRule( "FLOAT" , "-?[0-9]+\.[0-9]+([eE][\+-]?[0-9]+)?" );
lInt = LexerRule( "INT" , "-?[0-9]+" );
lOBracket = LexerRule( "OBRKT" , "{" );
lCBracket = LexerRule( "CBRKT" , "}" );

# When it comes to naming tokens, it's a good idea to keep them in UPPERCASE_WITH_UNDERSCORE
# So that they can be told about from the lowerCamelCase non-terminal symbols

# When constructing a lexer, the lexing rules given will be tested in the order given
# So make sure that you get your order right, else lexing errors will start to pop up.

lexer = Lexer( lNewline , lIgnore , lString , lIdent , lHex , lFloat , lInt ,
	lOBracket , lCBracket );

sourceFile = open( "lexerTestSource.txt" , "r" );	
source = sourceFile.read();
sourceFile.close();

tokens = lexer.lex( source );

if __name__ == "__main__": #Moved this code into a main wrapper since I want to import this test
	output = ""
	
	for token in tokens:
		print str( token )
		output += str( token ) + "\n";
	
	outputFile = open( "lexerTestOutput.txt" , "w" );
	outputFile.write( output );
	outputFile.close();
