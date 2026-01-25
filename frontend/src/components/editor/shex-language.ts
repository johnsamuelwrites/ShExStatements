/**
 * Monaco Editor language definition for ShExStatements.
 */

import type { languages } from 'monaco-editor';

export const SHEXSTATEMENTS_LANGUAGE_ID = 'shexstatements';
export const SHEX_LANGUAGE_ID = 'shex';

/**
 * ShExStatements language definition for Monaco Editor.
 */
export const shexstatementsLanguage: languages.IMonarchLanguage = {
  defaultToken: 'invalid',
  tokenPostfix: '.shexstatements',

  keywords: ['LITERAL', 'IRI', 'BNode', 'NonLiteral', 'CLOSED', 'EXTRA'],

  operators: ['|', '+', '*', '?', ','],

  brackets: [
    { open: '[', close: ']', token: 'delimiter.bracket' },
    { open: '{', close: '}', token: 'delimiter.brace' },
    { open: '<', close: '>', token: 'delimiter.angle' },
  ],

  tokenizer: {
    root: [
      // Comments
      [/#.*$/, 'comment'],

      // Prefixes (prefix|<uri>)
      [/^(\w+)(\|)(<[^>]+>)/, ['variable.prefix', 'delimiter', 'string.uri']],

      // Node names (@nodename)
      [/@\w+/, 'type.identifier'],

      // URIs
      [/<[^>]+>/, 'string.uri'],

      // Prefixed names (prefix:local)
      [/\w+:\w+/, 'variable.prefixed'],

      // Keywords
      [
        /\b(LITERAL|IRI|BNode|NonLiteral|CLOSED|EXTRA)\b/,
        {
          cases: {
            '@keywords': 'keyword',
            '@default': 'identifier',
          },
        },
      ],

      // Cardinality
      [/[+*?]/, 'operator.cardinality'],
      [/\{\d+,?\d*\}/, 'operator.cardinality'],

      // Delimiters
      [/\|/, 'delimiter.pipe'],
      [/,/, 'delimiter.comma'],
      [/;/, 'delimiter.semicolon'],

      // Numbers
      [/\d+/, 'number'],

      // Strings
      [/"[^"]*"/, 'string'],
      [/'[^']*'/, 'string'],

      // Whitespace
      [/\s+/, 'white'],

      // Identifiers
      [/\w+/, 'identifier'],
    ],
  },
};

/**
 * ShEx (output) language definition for Monaco Editor.
 */
export const shexLanguage: languages.IMonarchLanguage = {
  defaultToken: 'invalid',
  tokenPostfix: '.shex',

  keywords: [
    'PREFIX', 'BASE', 'IMPORT', 'start', 'LITERAL', 'IRI', 'BNode',
    'NonLiteral', 'CLOSED', 'EXTRA', 'LENGTH', 'MINLENGTH', 'MAXLENGTH',
    'MININCLUSIVE', 'MAXINCLUSIVE', 'MINEXCLUSIVE', 'MAXEXCLUSIVE',
    'TOTALDIGITS', 'FRACTIONDIGITS', 'AND', 'OR', 'NOT',
  ],

  operators: ['+', '*', '?', '=', '~', '//', '^'],

  brackets: [
    { open: '[', close: ']', token: 'delimiter.bracket' },
    { open: '{', close: '}', token: 'delimiter.brace' },
    { open: '(', close: ')', token: 'delimiter.paren' },
    { open: '<', close: '>', token: 'delimiter.angle' },
  ],

  tokenizer: {
    root: [
      // Comments
      [/#.*$/, 'comment'],

      // PREFIX declarations
      [/(PREFIX)(\s+)(\w+)(:)(\s*)(<[^>]+>)/, [
        'keyword',
        'white',
        'variable.prefix',
        'delimiter',
        'white',
        'string.uri',
      ]],

      // start declaration
      [/(start)(\s*)(=)/, ['keyword', 'white', 'operator']],

      // Shape references (@<name>)
      [/@<\w+>/, 'type.identifier'],

      // Shape definitions (<name>)
      [/<\w+>/, 'type.identifier'],

      // URIs
      [/<[^>]+>/, 'string.uri'],

      // Prefixed names
      [/\w+:\w+/, 'variable.prefixed'],

      // Keywords
      [
        /\b(PREFIX|BASE|IMPORT|start|LITERAL|IRI|BNode|NonLiteral|CLOSED|EXTRA|AND|OR|NOT)\b/,
        'keyword',
      ],

      // Cardinality
      [/[+*?]/, 'operator.cardinality'],
      [/\{\s*\d+\s*(,\s*\d*)?\s*\}/, 'operator.cardinality'],

      // Operators
      [/[=~]/, 'operator'],
      [/\/\//, 'operator'],
      [/\^/, 'operator'],

      // Delimiters
      [/[;,]/, 'delimiter'],
      [/[{}()\[\]]/, '@brackets'],

      // Numbers
      [/\d+/, 'number'],

      // Strings
      [/"[^"]*"/, 'string'],
      [/'[^']*'/, 'string'],

      // Whitespace
      [/\s+/, 'white'],

      // Identifiers
      [/\w+/, 'identifier'],
    ],
  },
};

/**
 * ShExStatements language configuration.
 */
export const shexstatementsLanguageConfiguration: languages.LanguageConfiguration = {
  comments: {
    lineComment: '#',
  },
  brackets: [
    ['[', ']'],
    ['{', '}'],
    ['<', '>'],
  ],
  autoClosingPairs: [
    { open: '[', close: ']' },
    { open: '{', close: '}' },
    { open: '<', close: '>' },
    { open: '"', close: '"' },
    { open: "'", close: "'" },
  ],
  surroundingPairs: [
    { open: '[', close: ']' },
    { open: '{', close: '}' },
    { open: '<', close: '>' },
    { open: '"', close: '"' },
    { open: "'", close: "'" },
  ],
};

/**
 * ShEx language configuration.
 */
export const shexLanguageConfiguration: languages.LanguageConfiguration = {
  comments: {
    lineComment: '#',
  },
  brackets: [
    ['[', ']'],
    ['{', '}'],
    ['(', ')'],
    ['<', '>'],
  ],
  autoClosingPairs: [
    { open: '[', close: ']' },
    { open: '{', close: '}' },
    { open: '(', close: ')' },
    { open: '<', close: '>' },
    { open: '"', close: '"' },
    { open: "'", close: "'" },
  ],
  surroundingPairs: [
    { open: '[', close: ']' },
    { open: '{', close: '}' },
    { open: '(', close: ')' },
    { open: '<', close: '>' },
    { open: '"', close: '"' },
    { open: "'", close: "'" },
  ],
};

/**
 * Common prefixes for autocomplete.
 */
export const COMMON_PREFIXES = [
  { prefix: 'rdf', uri: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#' },
  { prefix: 'rdfs', uri: 'http://www.w3.org/2000/01/rdf-schema#' },
  { prefix: 'xsd', uri: 'http://www.w3.org/2001/XMLSchema#' },
  { prefix: 'foaf', uri: 'http://xmlns.com/foaf/0.1/' },
  { prefix: 'schema', uri: 'http://schema.org/' },
  { prefix: 'dc', uri: 'http://purl.org/dc/elements/1.1/' },
  { prefix: 'dcterms', uri: 'http://purl.org/dc/terms/' },
  { prefix: 'owl', uri: 'http://www.w3.org/2002/07/owl#' },
  { prefix: 'skos', uri: 'http://www.w3.org/2004/02/skos/core#' },
  { prefix: 'wd', uri: 'http://www.wikidata.org/entity/' },
  { prefix: 'wdt', uri: 'http://www.wikidata.org/prop/direct/' },
  { prefix: 'wikibase', uri: 'http://wikiba.se/ontology#' },
];

/**
 * Node kind suggestions for autocomplete.
 */
export const NODE_KINDS = ['LITERAL', 'IRI', 'BNode', 'NonLiteral'];

/**
 * Cardinality suggestions for autocomplete.
 */
export const CARDINALITIES = [
  { label: '+', description: 'One or more' },
  { label: '*', description: 'Zero or more' },
  { label: '?', description: 'Zero or one' },
  { label: '{n}', description: 'Exactly n' },
  { label: '{n,m}', description: 'Between n and m' },
];
