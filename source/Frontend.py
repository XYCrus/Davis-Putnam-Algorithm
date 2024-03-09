#%%
import argparse

parser = argparse.ArgumentParser(description = "Front End for Davis-Putnam Algorithm Solver")

parser.add_argument('--InputFilePath', 
                    type = str, 
                    default = '../data/FrontEndInput.txt', 
                    help = "The path to the input file for processing.")

parser.add_argument('--OutputFilePath', 
                    type = str, 
                    default = '../data/FrontEndOutput.txt', 
                    help = "The path where the output file will be saved.")

args = parser.parse_args()

#%%
class Peg:
    def __init__(self, Hole, Time):
        self.Hole = Hole
        self.Time = Time

    def __repr__(self):
        return f"Peg({self.Hole},{self.Time})"

class Jump:
    def __init__(self, FromHole, OverHole, ToHole, Time):
        self.FromHole = FromHole
        self.OverHole = OverHole
        self.ToHole = ToHole
        self.Time = Time

    def __repr__(self):
        return f"Jump({self.FromHole},{self.OverHole},{self.ToHole},{self.Time})"

#%%
# Parse Input
def ReadInput(FilePath):
    with open(FilePath, 'r') as file:
        lines = file.read().splitlines()

    # First Line
    HoleCount, EmptyPos = map(int, lines[0].split())

    # Remaining Lines
    Rows = [tuple(map(int, line.split())) for line in lines[1:]]

    return HoleCount, EmptyPos, Rows

# Create all legit peg and jump
def PegNJump(HoleCount, Rows):
    # Legit Pegs
    Pegs = [Peg(hole, time) for time in range(1, HoleCount) for hole in range(1, HoleCount + 1)]

    # Legit Jumps
    Jumps = []
    for row in Rows:
        A, B, C = row
        for time in range(1, HoleCount - 1):  
            Jumps.append(Jump(A, B, C, time))
            Jumps.append(Jump(C, B, A, time))  

    return Pegs, Jumps

# Label to numerical value
def LabelObj(Pegs, Jumps):
    # Combine and Label
    Dummy = Jumps + Pegs
    ObjToNum = {repr(obj): i+1 for i, obj in enumerate(Dummy)}

    return ObjToNum

# Helper function to get numerical value
def Number(Obj, ObjToNum):
    return ObjToNum.get(repr(Obj), None)

# Precondition Axioms and Causal Axioms
def JumpEncoding(Jumps, ObjToNum):
    PreCauAx = []

    for jump in Jumps:
        JumpNum = Number(jump, ObjToNum)

        # Generating Peg objects and their number transformations for before and after the jump
        Pegs = [(Peg(jump.FromHole, jump.Time), 1),
                (Peg(jump.OverHole, jump.Time), 1),
                (Peg(jump.ToHole, jump.Time), -1), 
                (Peg(jump.FromHole, jump.Time + 1), -1),  
                (Peg(jump.OverHole, jump.Time + 1), -1),  
                (Peg(jump.ToHole, jump.Time + 1), 1)]

        # Creating result tuples
        results = [(-JumpNum, PN1 * Number(peg, ObjToNum)) for peg, PN1 in Pegs]

        PreCauAx.extend(results)

    return PreCauAx

# Frame Axioms
def PegEncoding(HoleCount, Jumps):
    FrameAx = []
    for i in range(1, HoleCount + 1):
        for j in range(1, HoleCount - 1):
            RelevantJumpsA = []
            RelevantJumpsB = []

            
            for jump in Jumps:
                if jump.FromHole == i and jump.Time == j:
                    RelevantJumpsA.append(jump)
                elif jump.OverHole == i and jump.Time == j:
                    RelevantJumpsA.append(jump)
                elif jump.ToHole == i and jump.Time == j:
                    RelevantJumpsB.append(jump)

            # if any
            if RelevantJumpsA:
                # Insert Pegs
                RelevantJumpsA.insert(0, Peg(i,j+1))
                RelevantJumpsA.insert(0, Peg(i,j))

                # Convert to number
                NumObj = [Number(obj, ObjToNum) for obj in RelevantJumpsA]
                NumObj[0] = -NumObj[0]
                
                FrameAx.append(NumObj)
            
            if RelevantJumpsB:
                # Insert Pegs
                RelevantJumpsB.insert(0, Peg(i,j+1))
                RelevantJumpsB.insert(0, Peg(i,j))

                # Convert to number
                NumObj = [Number(obj, ObjToNum) for obj in RelevantJumpsB]
                NumObj[1] = -NumObj[1]
                
                FrameAx.append(NumObj)

    return FrameAx

# One action at a time
def SingleJumpEncoding(Jumps, ObjToNum):
    OneAction = set()
    # Pick Jump of the same time
    for jump in Jumps:
        SameTimeJump = [dummy for dummy in Jumps if dummy.Time == jump.Time and dummy != jump]

        for dummy in SameTimeJump:
            # Sort to aviod duplicates
            OrderedPair = tuple(sorted([Number(jump, ObjToNum), Number(dummy, ObjToNum)]))
            OneAction.add((-OrderedPair[0], -OrderedPair[1]))

    return list(OneAction)

# Starting State
def StartState(EmptyPos, Pegs, ObjToNum):
    StartState = []

    EmptyPeg = Peg(EmptyPos, 1)
    StartState.append(-Number(EmptyPeg, ObjToNum))

    for peg in Pegs:
        if peg.Time == 1 and peg.Hole != EmptyPos:  
            StartState.append(Number(peg, ObjToNum))  
    
    return StartState

# Ending State
def EndState(HoleCount, Pegs, ObjToNum):
    EndState = []

    FinalPegs = [Number(peg, ObjToNum) for peg in Pegs if peg.Time == HoleCount - 1]

    # At least one peg remains at time N-1
    EndState.append(FinalPegs)

    # No two holes have a peg
    for i in range(len(FinalPegs)):
        for j in range(i + 1, len(FinalPegs)):
            EndState.append([-FinalPegs[i], -FinalPegs[j]])

    return EndState

def SaveNWrite(Jumps, Pegs, HoleCount, EmptyPos, ObjToNum, WriteFilePath):
    JumpClauses = JumpEncoding(Jumps, ObjToNum)
    PegClauses = PegEncoding(HoleCount, Jumps)
    SingleJumpClauses = SingleJumpEncoding(Jumps, ObjToNum)
    StartStateClauses = StartState(EmptyPos, Pegs, ObjToNum)
    EndStateClauses = EndState(HoleCount, Pegs, ObjToNum)
    
    # Combine all clauses
    combined_clauses = JumpClauses + PegClauses + SingleJumpClauses + StartStateClauses + EndStateClauses
    
    combined_clauses.append("0")
    
    # Add the labels along with jump/peg they belong to
    for obj, num in ObjToNum.items():
        combined_clauses.append(f"{num} {obj}")

    # Save to txt
    with open(WriteFilePath, 'w') as file:
        for clause in combined_clauses:
            # Parse Accordingly
            if isinstance(clause, tuple) or isinstance(clause, list):
                line = " ".join(str(num) for num in clause)
            else:
                line = str(clause)
            
            file.write(line + "\n")


#%%
if __name__ == '__main__': 
    HoleCount, EmptyPos, Rows = ReadInput(args.InputFilePath)

    Pegs, Jumps = PegNJump(HoleCount, Rows)
    
    ObjToNum = LabelObj(Pegs, Jumps)

    SaveNWrite(Jumps, Pegs, HoleCount, EmptyPos, ObjToNum, args.OutputFilePath)