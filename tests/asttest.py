from IceLeaf import *

ast = ASTObject( "name" , index=10 , name="bla" );
print str( ast )
ast.type = "hello"
print str( ast )
ast.name = 1337
print str( ast )
ast.index = "Drop the bomb"
print str( ast )
print ast.name