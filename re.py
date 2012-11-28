#!/usr/bin/env python

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
#
# Class-based example contributed to PLY by David McNab.
#
# Modified to use new-style classes.   Test case.
# -----------------------------------------------------------------------------

import sys
import nfa

if sys.version_info[0] >= 3:
    raw_input = input

import ply.lex as lex
import ply.yacc as yacc
import os

class Parser(object):
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()


    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = { }
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"
        #print self.debugfile, self.tabmodule

        # Build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def run(self):
        while 1:
            try:
                s = raw_input('re > ')
            except EOFError:
                break
            if not s: continue
            expr = yacc.parse(s)
            print expr
            nfa_input = expr.nfa()
            print nfa_input
            n = nfa.NFA(*nfa_input)
            print n
            d = n.to_dfa().rename()
            print d
            m = d.minimize().rename()
            print m
            while True:
                l = sys.stdin.readline().strip()
                print('"{0}" in DFA = {1}'.format(l, l in m))


counter = 0
def get_new_symbol():
    global counter
    counter += 1
    return counter

class Expression(object):
    def __init__(self, exprs):
        self.exprs = exprs;
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, ','.join([repr(x) for x in self.exprs]))
    def nfa(self):
        raise NotImplemented()

class Production(Expression):
    def nfa(self):
        left = self.exprs[0].nfa()
        left_start = left[3]
        left_end = left[4][0]

        start = get_new_symbol()
        end = get_new_symbol()
        states = left[0] + [start, end]

        alphabet = set(left[1]) | {''}
        trans = [((start, ''), left_start), ((left_end, ''), end),
                ((start, ''), end),  # Zero case
                ((left_end, ''), left_start)  # Production
                ] + left[2]
        return (states, alphabet, trans, start, [end])

class Symbol(Expression):
    def __repr__(self):
        return "(%s)" % (','.join([repr(x) for x in self.exprs]))
    def nfa(self):
        a = get_new_symbol()
        b = get_new_symbol()
        states = [a, b]
        alphabet = set([self.exprs[0]])
        trans = [((a, self.exprs[0]), b)]
        return (states, alphabet, trans, a, [b])

class Or(Expression):
    def nfa(self):
        left = self.exprs[0].nfa()
        right = self.exprs[1].nfa()
        left_start = left[3]
        right_start = right[3]
        left_end = left[4][0]
        right_end = right[4][0]

        start = get_new_symbol()
        end = get_new_symbol()
        states = left[0] + right[0] + [start, end]
        alphabet = set(left[1]) | set(right[1]) | {''}
        trans = ([((start, ''), left_start), ((start, ''), right_start)]
                + left[2] + right[2]
                + [((left_end, ''), end), ((right_end, ''), end)])
        return (states, alphabet, trans, start, [end])

class Concat(Expression):
    def nfa(self):
        left = self.exprs[0].nfa()
        right = self.exprs[1].nfa()
        left_start = left[3]
        right_start = right[3]
        left_end = left[4][0]
        right_end = right[4][0]
        states = left[0] + right[0]

        alphabet = set(left[1]) | set(right[1]) | {''}
        trans = left[2] + [((left_end, ''), right_start)] + right[2]
        return (states, alphabet, trans, left_start, [right_end])

class Calc(Parser):

    tokens = (
        'CHAR', 'PLUS', 'STAR', 'LPAREN','RPAREN',
        )

    # Tokens

    t_CHAR    = r'[a-zA-Z0-9_]'
    t_PLUS    = r'\+'
    t_STAR    = r'\*'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'

    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Parsing rules

    precedence = (
        #('left', 'PLUS'),
        ('left', 'CONCAT'),
        ('left', 'STAR'),
        )

    def p_expression_concat(self, p):
        """
        expression : expression expression %prec CONCAT
        """
        p[0] = Concat([p[1], p[2]])

    def p_expression_star(self, p):
        """
        expression : expression STAR
        """
        p[0] = Production([p[1]])

    def p_expression_binop(self, p):
        """
        expression : expression PLUS expression
        """
        ##print [repr(p[i]) for i in range(0,4)]
        #if p[2] == '+'  : p[0] = p[1] + p[3]
        #elif p[2] == '-': p[0] = p[1] - p[3]
        #elif p[2] == '*': p[0] = p[1] * p[3]
        #elif p[2] == '/': p[0] = p[1] / p[3]
        #elif p[2] == '**': p[0] = p[1] ** p[3]
        p[0] = Or([p[1], p[3]])

    #def p_expression_uminus(self, p):
    #    'expression : MINUS expression %prec UMINUS'
    #    p[0] = -p[2]

    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        #p[0] = Expression([p[2]])
        p[0] = p[2]

    def p_expression_number(self, p):
        'expression : CHAR'
        p[0] = Symbol([p[1]])

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

if __name__ == '__main__':
    calc = Calc(debug=1)
    calc.run()
