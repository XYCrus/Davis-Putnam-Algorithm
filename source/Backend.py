#%%
import argparse

parser = argparse.ArgumentParser(description = "Back End for Davis-Putnam Algorithm Solver")

parser.add_argument('--InputFilePath', 
                    type = str, 
                    default = '../data/DPOutput.txt', 
                    help = "The path to the input file for processing.")

parser.add_argument('--OutputFilePath', 
                    type = str, 
                    default = '../data/BackEndOutput.txt', 
                    help = "The path where the output file will be saved.")

args = parser.parse_args()

#%%
# Check value before 0, matching after 0
def ReadNParse(FilePath):
    with open(FilePath, 'r') as file:
        ReadTruth = True
        TempIndex = []
        Output = []

        for line in file:
            line = line.strip()
            # All TF before 0
            if line == "0":
                ReadTruth = False
                continue
            
            # Before 0, read
            if ReadTruth:
                number, value = line.split()
                if value == 'T': 
                    TempIndex.append(int(number))

            # After 0, compare index
            else:
                Parts = line.split()

                if Parts[1].startswith('Jump'):
                    JumpNum = int(Parts[0])
                    # If this jump's number is in TempIndex, append to Output
                    if JumpNum in TempIndex:
                        Output.append(Parts[1])

        return Output

# Helper function to sort
def SortKey(Jump):
    return int(Jump.split(',')[-1].rstrip(')'))

# Sort based on time, then output to txt
def OrderNWrite(Output, OutputFilePath):
    SortedOutput = sorted(Output, key = SortKey)

    with open(OutputFilePath, 'w') as output_file:
        for line in SortedOutput:
            output_file.write(line + '\n')

#%%
if __name__ == '__main__':
    Output = ReadNParse(args.InputFilePath)
    OrderNWrite(Output, args.OutputFilePath)