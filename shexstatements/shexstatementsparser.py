#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ply import lex
from ply import yacc
from .errors import UnrecognizedCharacterError, ParserError
from .shexstatement import Node, NodeKind, Value, ValueList, Type, TypeList, Cardinality, ShExStatement, ShExStatements

class ShExStatementLexerParser(object):
  tokens = (
    'COLON',
    'COMMA',
    'CLOSED',
    'EXTRA',
    'COMMENT',
    'SEPARATOR',
    'STRING',
    'TYPESTRING',
    'NODEKIND',
    'IMPORTSTRING',
    'NUMBER',
    'NODENAME',
    'PERIOD',
    'CARET',
    'PLUS',
    'STAR',
    'QUESTIONMARK',
    'LSQUAREBRACKET',
    'RSQUAREBRACKET',
    'NEWLINE',
    'SPACE'
  )
  def __init__(self, debug=False):
    self.debug = debug
    self.node = None
    self.comment = ""
    self.imports = []
    self.prefixes = []
    self.prop = None
    self.values = None
    self.cardinality = None
    self.statement = []
    self.shapeconstraints = []
    self.statements = ShExStatements([])

  def t_COLON(self, t):
    r':'
    return t

  def t_SEPARATOR(self, t):
    r'\|'
    return t

  def t_COMMA(self, t):
    r'\,'
    return t

  def t_PERIOD(self, t):
    r'\.'
    return t

  def t_PLUS(self, t):
    r'\+'
    return t

  def t_QUESTIONMARK(self, t):
    r'\?'
    return t

  def t_STAR(self, t):
    r'\*'
    return t

  def t_CARET(self, t):
    r'\^'
    return t

  def t_NUMBER(self, t):
    r'\d+'
    return t

  def t_IMPORTSTRING(self, t):
    r'@@@[^@{}\[\]\,\|\s\^]+'
    return t

  def t_NODENAME(self, t):
    r'@[^\@{}\[\]\,\.\|\s\^]+'
    return t

  def t_COMMENT(self, t):
    r'\#[^\n]*'
    return t

  def t_CLOSED(self, t):
    r'(CLOSED|><)'
    return t

  def t_EXTRA(self, t):
    r'([Ee][Xx][Tt][Rr][Aa])'
    return t

  def t_NODEKIND(self, t):
    # Allowing Literal, BNode, NonLiteral, IRI
    r'([Ll][Ii][Tt][Ee][Rr][Aa][Ll]|[Ii][Rr][Ii]|[Bb][Nn][Oo][Dd][Ee]|[Nn][Oo][Nn][Ll][Ii][Tt][Ee][Rr][Aa][Ll])'
    return t

  def t_STRING(self, t):
    r'[^@{}\[\]\,\|\s\^]+'
    return t

  # To specify types
  def t_TYPESTRING(self, t):
    r'@@[^@{}:\[\]\,\|\s\^]+'
    return t

  def t_SPACE(self, t):
    r'[ \t]+'

  def t_LSQUAREBRACKET(self, t):
    r'\['
    return t
  
  def t_RSQUAREBRACKET(self, t):
    r'\]'
    return t

  def t_NEWLINE(self,t):
    r'[\n\r\f\v]+'
    t.lexer.lineno += len(t.value)
    self.lineno = t.lexer.lineno

  def t_error(self, t):
    print("Unrecognized character '%s'" %t.value[0])
    raise UnrecognizedCharacterError("unrecognized character error")

  def build(self,**kwargs):
     self.lexer = lex.lex(module=self, **kwargs)
  
  def lexer(self):
     return self.lexer

  def input(self, data):
    tokens = []
    self.lexer.input(data)
    while True:
      token = self.lexer.token()
      if not token:
        break
      tokens.append(token)  
    return tokens

  precedence =  (
    ('left', 'SEPARATOR'),
  )

  def p_statements(self, p):
    '''
       statements : SPACE
             | NEWLINE
             | statement
             | statement statements
             | prefixes statement statements
             | imports prefixes statement statements'''
    if (self.debug): 
      print("ShEx Statements")
    self.statements.add_prefixes(self.prefixes)
    self.statements.add_imports(self.imports)
    self.node = None
    self.comment = ""
    self.imports = []
    self.prefixes = []
    self.prop = None
    self.values = None
    self.cardinality = None
    self.statement = []

  def p_statement(self, p):
    '''
       statement : shapeconstraint
             | shapeconstraint SEPARATOR comment
             | nodeproperty propertyvalue 
             | nodeproperty propertyvalue SEPARATOR comment
             | nodeproperty delimseparatedlist
             | nodeproperty delimseparatedlist SEPARATOR comment
             | nodeproperty propertyvalue SEPARATOR cardinality
             | nodeproperty propertyvalue SEPARATOR cardinality SEPARATOR comment
             | nodeproperty LSQUAREBRACKET value RSQUAREBRACKET
             | nodeproperty LSQUAREBRACKET value RSQUAREBRACKET SEPARATOR comment
             | nodeproperty LSQUAREBRACKET delimseparatedlist RSQUAREBRACKET
             | nodeproperty LSQUAREBRACKET delimseparatedlist RSQUAREBRACKET SEPARATOR comment
             '''
    if (self.debug): 
      print("ShEx Statement")
    self.statement = ShExStatement(self.node, self.prop, self.values, self.cardinality, self.comment)
    self.statements.add(self.statement)
    self.node = None
    self.comment = ""
    self.shapeconstraints = []
    self.prop = None
    self.values = None
    self.cardinality = None

  def p_shapeconstraint(self, p):
    '''shapeconstraint : node SEPARATOR CLOSED
                       | node SEPARATOR PLUS PLUS SEPARATOR value
                       | node SEPARATOR EXTRA SEPARATOR value'''
    if (self.debug): 
      print("shapeconstraint " + str(p))
    if(len(p) > 3):
      if(p[3].lower() == "closed" or p[3] == "><"):
        self.prop = "CLOSED"
      else:
        self.prop = "EXTRA"

  def p_nodeproperty(self, p):
    '''nodeproperty : node SEPARATOR prop SEPARATOR'''
    if (self.debug): 
      print("nodeproperty " + str(p))

  def p_prefixes(self, p):
    '''prefixes : prefix
                     | prefix prefixes'''
    if (self.debug): 
      print("prefixes " + str(p))

  def p_imports(self, p):
    '''imports : import
                     | import imports'''
    if (self.debug): 
      print("imports " + str(p))

  def p_prefix(self, p):
    '''prefix : STRING SEPARATOR STRING'''
    if (self.debug): 
      print("prefixes " + str(p))
    self.prefixes.append((p[1],p[3]))

  def p_import(self, p):
    '''import : IMPORTSTRING'''
    if (self.debug): 
      print("import " + str(p))
    self.imports.append(p[1][3:])

  def p_propertyvalue(self, p):
    '''propertyvalue : value
                     | node
                     | type
                     | specialterm'''
    if (self.debug): 
      print("propertyvalue " + str(p))

  def p_node(self, p):
    '''node : NODENAME
                 | NODENAME COLON STRING 
    '''
    if (self.debug): 
      print("node " + str(p))
    if not self.node:
      if (len(p) < 3): 
        self.node = Node(p[1])
      else:
        self.node = Node(p[1]+":"+p[3])
    else:
      if (len(p) < 3): 
        self.values = Node(p[1])
      else:
        self.values = Node(p[1]+":"+p[3])

  def p_specialterm(self, p):
    '''specialterm : PERIOD
                   | NODEKIND
    '''
    if (self.debug): 
      print("specialterm " + str(p))
    self.values = NodeKind(p[1]) 

  def p_cardinality(self, p):
    '''cardinality : PLUS
                | STAR
                | QUESTIONMARK
                | NUMBER
                | NUMBER COMMA
                | NUMBER COMMA NUMBER
    '''
    if (self.debug): 
      print("cardinality " + str(p))
    if (len(p) == 2):
     self.cardinality = p[1]
    if (len(p) == 3):
     self.cardinality = p[1] + p[2]
    elif (len(p) == 4):
     self.cardinality = p[1] + p[2] + p[3]

  def p_type(self, p):
    '''type : TYPESTRING
            | TYPESTRING COLON STRING'''
    if (self.debug): 
      print("type " + str(p))
    if not self.values:
      self.values = TypeList([])
    if (len(p) == 4):
      self.values.add(Type(p[1]+":"+p[3]))
    else:
      self.values.add(Type(p[1]))

  def p_value(self, p):
    '''value : STRING'''
    if (self.debug): 
      print("value " + str(p))

    if not self.values:
      self.values = ValueList([])
    if (len(p) == 4):
      self.values.add(Value(p[1]+":"+p[3]))
    else:
      self.values.add(Value(p[1]))

  def p_comment(self, p):
    '''comment : COMMENT'''
    if (self.debug): 
      print("comment " + str(p))
    self.comment = p[1]

  def p_prop(self, p):
    '''prop : value
            | CARET value'''
    if (self.debug): 
      print("prop " + str(p))
    # One value is already present
    if(len(p) == 2):
       self.prop = str(self.values.get_value_list()[0])
    else:
      self.prop = "^" + str(self.values.get_value_list()[0])
    self.values = None

  def p_commaseparatedvaluelist(self, p):
    '''commaseparatedvaluelist : value COMMA value
                | value COMMA commaseparatedvaluelist'''
    if (self.debug): 
      print("commaseparatedvaluelist " + str(p))

  def p_commaseparatedtypelist(self, p):
    '''commaseparatedtypelist : type COMMA type
                | type COMMA commaseparatedtypelist'''
    if (self.debug): 
      print("commaseparatedtypelist " + str(p))

  def p_delimseparatedlist(self, p):
    '''delimseparatedlist : commaseparatedtypelist
                | commaseparatedvaluelist'''
    if (self.debug): 
      print("delimseparatedlist " + str(p))

  def p_error(self, p):
    lineno = 0
    if (self.debug and p):
      lineno = p.lineno
      print(p.lexpos, p.lineno, str(p), p.value)
    raise ParserError("Syntax error in input data: Line no: %d, Error: %s" % (lineno, str(p)))

  def buildparser(self,**kwargs):
     self.lexer = lex.lex(module=self, **kwargs)
     self.parser = yacc.yacc(module=self, **kwargs)
     

  def parse(self, data):
    result = self.parser.parse(data, lexer=self.lexer, tracking=True)
    if (self.debug): 
      print(result)
    return self.statements

