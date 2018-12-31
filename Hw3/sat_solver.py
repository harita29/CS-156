import sys
import re

def dpllSat(clauses):
    symbols = getSymbolsClauses(clauses)
    return dpll(clauses, symbols, {});

def dpll(clauses, symbols, assignment):
    print "Symbols"
    print symbols
    print "Assignment"
    print assignment

    if checkAllClausesTrue(clauses, assignment):
        return assignment
    if checkForFalseClause(clauses, symbols, assignment):
        return False
    literal = findPureSymbol(symbols)
    if literal:
        assignment.update({literal:1, -literal:-1})
        return dpll(clauses, 
                    {key:val for key, val in symbols.items() if val != literal and val != -literal},
                    assignment)
    literal = findUnitClause(clauses, assignment)
    if literal:
        assignment.update({literal:1, -literal:-1})
        return dpll(clauses,
                    {key:val for key, val in symbols.items() if val != literal and val != -literal},
                    assignment)

    literal = choose(symbols)
    symbols = {key:val for key, val in symbols.items() if val != literal and val != -literal}
    assignment.update({literal:1, -literal:-1})
    sat_assignment = dpll(clauses, symbols, assignment)
    if sat_assignment == False and type(sat_assignment) == type(False):
        assignment.update({literal:-1, -literal:1})
        sat_assignment = dpll(clauses, symbols, assignment)
    return sat_assignment


def getSymbolsClauses(clauses):
    symbols = {}
    for clause in clauses:
        for literal in clause:
            symbols[literal] = literal
    return symbols

def checkAllClausesTrue(clauses, assignment):
    for clause in clauses:
        value = False
        for literal in clause:
            if literal in assignment and assignment[literal] > 0:
                value = True
                break
        if not value:
            return False
    return True

def checkForFalseClause(clauses, symbols, assignment):
    for clause in clauses:
        value = True
        for literal in clause:
            if literal in symbols:
                value = False
                break
            if literal in assignment and assignment[literal] > 0:
                value = False
                break
        if value:
            return True
    return False


def findPureSymbol(symbols):
    for literal in symbols.itervalues():
        new_literal = literal * -1
        if new_literal not in symbols:
            return literal
    return False


def findUnitClause(clauses, assignment):
    assigned_literals = assignment.keys()
    for clause in clauses:
        unassigned = [item for item in clause if item not in assigned_literals]
        if len(unassigned) == 1:
            already_true = False;
            for literal in clause:
                if literal in assignment and assignment[literal] > 0:
                    already_true = True
                    break
            if not already_true:
                return unassigned.pop()
    return False


def choose(symbols):
    return symbols.popitem()[1]

my_help_str = """
              sat_solver is a program used to read in a set of clauses in satcompetition.org
              and output whether it is satisfiable or not. It is run from the command line
              using the syntax:
              php sat_solver.php filename
              """

if len(sys.argv) < 2:
    print my_help_str

lines = open(sys.argv[1]).readlines()
clauses = []

for line in lines:
    line = line.strip()
    if line[0] == 'c' or line[0] == 'p':
        continue
    pre_clause = re.split("\s+", line)
    clause = []
    for pre_literal in pre_clause:
        literal = int(pre_literal)
        if literal != 0:
            clause.append(literal)
    if clause:
        clauses.append(clause)

print "Clauses"
print clauses
print dpllSat(clauses)
