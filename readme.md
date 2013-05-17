IceLeaf
=======
**IceLeaf** is a pure python library for lexing, parsing and AST handling.
It is not written to be faster or more shiny than libraries like [PLY](http://www.dabeaz.com/ply/), it focuses on being easy to learn and use.

features:
---------
**IceLeaf** will support some basic, but useful features like:

  * Regex based lexeing. You will be able to define lexer rules, specifying the token type, token channel and such.
  * A simple and extendable parsing engine, for custom parsers ( using token reading functions )
  * A [context free grammar](http://en.wikipedia.org/wiki/Context_free_grammar) based parser.
  * (Hopefully) A file format for writing grammars even faster ( It's a parser parser )
  * Useful functions for treating `dict`s as [ASTs](http://en.wikipedia.org/wiki/Abstract_syntax_tree). ( Maybe even implement a real AST class )
 
examples:
---------
Nothing yet here

Credits and special thanks:
---------------------------
I'll like to thank the Python team, for quite obvious reasons :)
