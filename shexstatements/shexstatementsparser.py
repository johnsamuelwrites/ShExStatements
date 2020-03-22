#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ply import lex
from ply import yacc
from .errors import UnrecognizedCharacterError, ParserError
from .shexstatement import Node, NodeKind, Value, ValueList, Cardinality, ShExStatement, ShExStatements

class ShExStatementLexerParser(object):
  tokens = (
    'COLON',
    'COMMA',
    'COMMENT',
    'SEPARATOR',
    'STRING',
    'NODEKIND',
    'NUMBER',
    'NODENAME',
    'PERIOD',
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
    self.prefixes = []
    self.prop = None
    self.values = None
    self.cardinality = None
    self.statement = []
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

  def t_NUMBER(self, t):
    r'\d+'
    return t

  def t_NODENAME(self, t):
    r'@[^\#@{}\[\],\.\|\s]+'
    return t

  def t_COMMENT(self, t):
    r'\#[\w \t]*'
    return t

  def t_NODEKIND(self, t):
    r'(LITERAL|IRI|BNode)'
    return t

  def t_STRING(self, t):
    r'[^@{}\[\],\|\s]+'
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
    r'\n+'
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
       statements : statement
             | SPACE 
             | statement statements
             | prefixes statement statements'''
    if (self.debug): 
      print("ShEx Statements")
    self.statements.add_prefixes(self.prefixes)
    self.node = None
    self.comment = ""
    self.prefixes = []
    self.prop = None
    self.values = None
    self.cardinality = None
    self.statement = []

  def p_statement(self, p):
    '''
       statement : nodeproperty propertyvalue 
             | nodeproperty propertyvalue SEPARATOR comment
             | nodeproperty commaseparatedvaluelist
             | nodeproperty commaseparatedvaluelist SEPARATOR comment
             | nodeproperty spaceseparatedvaluelist
             | nodeproperty spaceseparatedvaluelist SEPARATOR comment
             | nodeproperty propertyvalue SEPARATOR cardinality
             | nodeproperty propertyvalue SEPARATOR cardinality SEPARATOR comment
             | nodeproperty LSQUAREBRACKET value RSQUAREBRACKET
             | nodeproperty LSQUAREBRACKET value RSQUAREBRACKET SEPARATOR comment
             | nodeproperty LSQUAREBRACKET commaseparatedvaluelist RSQUAREBRACKET
             | nodeproperty LSQUAREBRACKET commaseparatedvaluelist RSQUAREBRACKET SEPARATOR comment
             | nodeproperty LSQUAREBRACKET spaceseparatedvaluelist RSQUAREBRACKET
             | nodeproperty LSQUAREBRACKET spaceseparatedvaluelist RSQUAREBRACKET SEPARATOR comment
             '''
    if (self.debug): 
      print("ShEx Statement")
    self.statement = ShExStatement(self.node, self.prop, self.values, self.cardinality, self.comment)
    self.statements.add(self.statement)
    self.node = None
    self.comment = ""
    self.prop = None
    self.values = None
    self.cardinality = None

  def p_nodeproperty(self, p):
    '''nodeproperty : node SEPARATOR prop SEPARATOR'''
    if (self.debug): 
      print("nodeproperty " + str(p))

  def p_prefixes(self, p):
    '''prefixes : prefix
                     | prefix prefixes'''
    if (self.debug): 
      print("prefixes " + str(p))

  def p_prefix(self, p):
    '''prefix : STRING SEPARATOR STRING'''
    if (self.debug): 
      print("prefixes " + str(p))
    self.prefixes.append((p[1],p[3]))

  def p_propertyvalue(self, p):
    '''propertyvalue : value
                     | node
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
                | NUMBER COMMA NUMBER
    '''
    if (self.debug): 
      print("cardinality " + str(p))
    self.cardinality = p[1]

  def p_value(self, p):
    '''value : STRING
                | STRING COLON STRING'''
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
    '''prop : value'''
    if (self.debug): 
      print("prop " + str(p))
    # One value is already present
    self.prop = str(self.values.get_value_list()[0])
    self.values = None

  def p_commaseparatedvaluelist(self, p):
    '''commaseparatedvaluelist : value COMMA value
                | value COMMA commaseparatedvaluelist'''
    if (self.debug): 
      print("valuelist " + str(p))

  def p_spaceseparatedvaluelist(self, p):
    '''spaceseparatedvaluelist : value value
                | value SPACE spaceseparatedvaluelist'''
    if (self.debug): 
      print("valuelist " + str(p))

  def p_error(self, p):
    if (self.debug and p):
      print(p.lexpos, p.lineno, str(p), p.value)
    raise ParserError("Syntax error in input data: Line no: %d, Error: %s" % (p.lineno, str(p)))

  def buildparser(self,**kwargs):
     self.lexer = lex.lex(module=self, **kwargs)
     self.parser = yacc.yacc(module=self, **kwargs)
     

  def parse(self, data):
    result = self.parser.parse(data, lexer=self.lexer, tracking=True)
    if (self.debug): 
      print(result)
    return self.statements

