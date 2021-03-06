![IceLeaf](/iceleaf.png)IceLeaf
=======
**IceLeaf** is a pure python library for lexing, parsing and AST handling.
It is not written to be faster or more shiny than libraries like [PLY](http://www.dabeaz.com/ply/), it focuses on being easy to learn and use.

Features:
---------
**IceLeaf** will support some basic, but useful features like:

  * Regex based lexeing. You will be able to define lexer rules, specifying the token type, token channel and such.
  * A simple and extendable parsing engine, for custom parsers ( using token reading functions )
  * A lightweight AST class for productivity and ease of use ( It's just a fancy `dict` ).

Examples:
---------
I will put some code examples in here, but until then look in the ```tests``` folder,
it should be fairly documented.

Used in project(s):
-----------------
  * [DarkMatter](https://github.com/thebreadcat/DarkMatter), A programming langauge designed for the DCPU-16 ( By me )

Credits and special thanks:
---------------------------
I'll like to thank the Python team, for quite obvious reasons :)
