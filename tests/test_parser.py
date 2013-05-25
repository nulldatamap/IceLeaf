from IceLeaf import *
import test_lex

tokens = test_lex.tokens; #Just import the lexed source from our previous test

class TestParser(Parser):
	def __init__( self ):
		Parser.__init__( self );
	
	def parse( self , tokens ): 
		Parser.parse( self , tokens ); #Call the superclass
		ast = ASTObject( "program" , head= [] , body= [] );
		ast.head.append( self.expect( "IDENT" ).data ); #Expect an IDENT token, and fail otherwise
		while self.matches("IDENT"): #While the current token is still a IDENT
			ast.head.append( self.next().data ); #Add it to our header list
		self.expect( "OBRKT" ); #Body start
		print str( self.lookahead( 2 ) );
		while not self.matches( "CBRKT" ): #As long as we don't match the closing bracket
			ast.body.append( self.entry(  ) ); #Parse a body entry
		
		self.expect( "CBRKT" ); #Body end
		self.matches( "EOF" ); #And that should be the end of the file
		return ast;
	
	def entry( self ):
		ast = ASTObject( "entry" , name= "" , values= [] );
		ast.name = self.expect( "IDENT" ).data;
		self.expect( "OBRKT" );
		while not self.matches( "CBRKT" ):
			ast.values.append( self.literal() );
		self.expect( "CBRKT" )
		return ast;
	
	def literal( self ):
		literals = [ "INT" , "STRING" , "FLOAT" , "HEX" ]
		v = False;
		i = 0;
		while not v: #Iterate through the different literal types
			v = self.nextif( literals[i] );
			i += 1;
			if i == len( literals ) and not v: #If all fail
				raise ParserError( self.cur() , "a valid literal!" ); #Raise error: "expected valid literal"
		return v.data;

# The AST structure will look a little like this:
#            _________
#           | program |
#           |_________|
#                / \
#              /     \
#            /         \
#  ________/__________  \
# | head [ IDENT .. ] |   \____________________
# |___________________|   | body [ entry ... ] |
#                         |____________________|
#                           
#                          _______
#                         | entry |
#                         |_______|
#                        /     \
#          _____________/       \_______________________
#          | name IDENT |       | values [ literal .. ] |
#          |____________|       |_______________________|
#
#                                 _______________________
#                                | literal STRING / INT  |
#                                | / FLOAT / HEX         |
#                                |_______________________|

parser = TestParser();
ast = parser.parse( tokens );

if __name__ == "__main__":
	tostring = "";
	
	tostring += str( ast.head );
	tostring += "\n{\n";
	for entry in ast.body:
		tostring += "    " + entry.name + " "
		tostring += str( entry.values ) + "\n";
	tostring += "}\n"
	
	print tostring;
	outputfile = open( "parserTestOutput.txt" , "w" );
	outputfile.write( tostring );
	outputfile.close();


