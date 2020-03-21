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
    'WHITESPACE',
    'SPACE'
  )
  def __init__(self, debug=True):
    self.debug = debug
    self.node = None
    self.comment = ""
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
    r'@\w+'
    return t

  def t_COMMENT(self, t):
    r'\#[^\n]*'
    return t

  def t_NODEKIND(self, t):
    r'(LITERAL|IRI|BNode)'
    return t

  def t_STRING(self, t):
    r'[^@{}\[\],\:\|\s]+'
    return t

  def t_SPACE(self, t):
    r'[ \t]+'
    return t

  def t_WHITESPACE(self, t):
    r'\s+'

  def t_LSQUAREBRACKET(self, t):
    r'\['
    return t
  
  def t_RSQUAREBRACKET(self, t):
    r'\]'
    return t

  def t_NEWLINE(self,t):
    r'\n+'
    t.lexer.lineno += len(t.value)

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
    ('left', 'COLON'),
    ('left', 'STAR', 'PLUS'),
    ('left', 'COMMA'),
    ('left', 'SEPARATOR'),
    ('left', 'LSQUAREBRACKET', 'RSQUAREBRACKET'),
  )

  def p_statements(self, p):
    '''
       statements : statement
             | statement SEPARATOR comment
             | statement statements'''
    if (self.debug): 
      print("ShEx Statements")
    self.node = None
    self.comment = ""
    self.prop = None
    self.values = None
    self.cardinality = None
    self.statement = []

  def p_statement(self, p):
    '''
       statement : firstnode SEPARATOR prop SEPARATOR value
             | firstnode SEPARATOR prop SEPARATOR secondnode
             | firstnode SEPARATOR prop SEPARATOR specialterm
             | firstnode SEPARATOR prop SEPARATOR commaseparatedvalueset
             | firstnode SEPARATOR prop SEPARATOR spaceseparatedvalueset
             | firstnode SEPARATOR prop SEPARATOR secondnode SEPARATOR cardinality
             | firstnode SEPARATOR prop SEPARATOR value SEPARATOR cardinality
             | firstnode SEPARATOR prop SEPARATOR specialterm SEPARATOR cardinality
             | firstnode SEPARATOR prop SEPARATOR LSQUAREBRACKET value RSQUAREBRACKET
             | firstnode SEPARATOR prop SEPARATOR LSQUAREBRACKET commaseparatedvalueset RSQUAREBRACKET
             | firstnode SEPARATOR prop SEPARATOR LSQUAREBRACKET spaceseparatedvalueset RSQUAREBRACKET
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

  def p_firstnode(self, p):
    '''firstnode : NODENAME
                 | NODENAME COLON STRING 
    '''
    if (self.debug): 
      print("firstnode " + str(p))
    if (len(p) < 3): 
      self.node = Node(p[1])
    else:
      self.node = Node(p[1]+":"+p[3])
    self.values = None

  def p_secondnode(self, p):
    '''secondnode : NODENAME
                  |  NODENAME COLON STRING 
    '''
    if (self.debug): 
      print("secondnode " + str(p))
    if not self.values:
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
    '''prop : STRING
                | STRING COLON STRING'''
    if (self.debug): 
      print("prop " + str(p))
    if (len(p) == 4):
      self.prop = p[1] + ":" + p[3]
    else:
      self.prop = p[1]

  def p_commaseparatedvalueset(self, p):
    '''commaseparatedvalueset : value COMMA value
                | value COMMA commaseparatedvalueset'''
    if (self.debug): 
      print("valueset " + str(p))

  def p_spaceseparatedvalueset(self, p):
    '''spaceseparatedvalueset : value SPACE
                | value SPACE value
                | value SPACE spaceseparatedvalueset'''
    if (self.debug): 
      print("valueset " + str(p))

  def p_error(self, p):
    if (self.debug and p):
      print(p.lexpos, p.lineno, str(p), p.value)
    raise ParserError("Syntax error in input data: %s" % str(p))

  def buildparser(self,**kwargs):
     self.lexer = lex.lex(module=self, **kwargs)
     self.parser = yacc.yacc(module=self, **kwargs)
     

  def parse(self, data):
    result = self.parser.parse(data, lexer=self.lexer)
    if (self.debug): 
      print(result)
    return self.statements

