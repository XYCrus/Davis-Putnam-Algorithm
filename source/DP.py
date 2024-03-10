#%%
import argparse

parser = argparse.ArgumentParser(description = "Davis-Putnam Algorithm Solver")

parser.add_argument('--InputFilePath', 
                    type = str, 
                    default = '../data/FrontEndoutput.txt', 
                    help = "The path to the input file for processing.")

parser.add_argument('--OutputFilePath', 
                    type = str, 
                    default = '../data/DPOutput.txt', 
                    help = "The path where the output file will be saved.")

args = parser.parse_args()

#%%
# Read txt file and set up variable for DP
def ReadNParse(FilePath):
    with open(FilePath, 'r') as file:
        Clauses = []
        Aux = ""
        ReadClause = True

        for line in file:
            line = line.strip()
            # All clauses before 0
            if line == "0":
                ReadClause = False
                continue
            
            # Before 0, read
            if ReadClause:
                clause = [int(x) for x in line.split()]
                Clauses.append(clause)

            # After 0, store as auxiliary info
            else:
                Aux += line + '\n'

        return Clauses, Aux.strip()

# Helper function to check whether singleton exist at each step
def ExistSingleton(Clauses):
    Singleton = [clause for clause in Clauses if len(clause) == 1]
    if Singleton:
        return True, Singleton
    else:
        return False, []

# Propagate the assignment through the clauses, simplifying them
def Propagate(Clauses, Atom, Value):
    NewClauses = []
    for clause in Clauses:
        # Clause satisfied and skiped
        if Atom in clause and Value:
            continue  

        # Clause satisfied by negation and skiped
        elif -Atom in clause and not Value:
            continue 

        # Remove the atom or its negation from the clause 
        else:
            NewClause = [lit for lit in clause if lit != Atom and lit != -Atom]
            NewClauses.append(NewClause)

    return NewClauses

# Recursive function to find assignments
def DPHelper(Clauses, Values, Atoms):
    HasSingleton, Singletons = ExistSingleton(Clauses)
    
    while HasSingleton:
        for singleton in Singletons:
            lit = singleton[0]
            Atom = abs(lit)
            Value = lit > 0
            Values[Atom] = Value

            # Mark atom as assigned
            if Atom in Atoms: Atoms.remove(Atom)  

            Clauses = Propagate(Clauses, Atom, Value)

        HasSingleton, Singletons = ExistSingleton(Clauses)

    # All clauses satisfied
    if not Clauses:  
        return Values
    
    # Empty clause, unsatisfiable
    if any(len(clause) == 0 for clause in Clauses):  
        return None 

    # Choose an unassigned atom and try both T and F
    Atom = next(iter(Atoms))
    for Value in [True, False]:
        new_Values = Values.copy()
        new_Values[Atom] = Value
        new_Atoms = Atoms.copy()
        new_Atoms.remove(Atom)

        result = DPHelper(Propagate(Clauses, Atom, Value), 
                          new_Values, 
                          new_Atoms)

        # Satisfying assignment found
        if result is not None:  
            return result

    # No satisfying assignment found
    return None

# Entry point of DP recursive function
def DP(Clauses):
    Values = {}
    Atoms = set(abs(literal) for clause in Clauses for literal in clause)
    Assignments = DPHelper(Clauses, Values, Atoms)

    return Assignments
    
# Parse out and output to txt
def ParseNWrite(Assignments, Aux, OutputFilePath):
    with open(OutputFilePath, 'w') as file:
        if Assignments:
            AssignmentsSorted = dict(sorted(Assignments.items()))
            for atom, value in AssignmentsSorted.items():
                file.write(f"{atom} {'T' if value else 'F'}\n")
            file.write("0\n")
            file.write(Aux)
        else:
            file.write("0\n" + Aux)
    

#%%
if __name__ == '__main__':
    Clauses, Aux = ReadNParse(args.InputFilePath)

    Assignments = DP(Clauses)

    ParseNWrite(Assignments, Aux, args.OutputFilePath)

