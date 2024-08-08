import argparse
import os

parser = argparse.ArgumentParser(description='--M <width> --N <width> --type <wallace/dadda/RoCoCo> --signed 0/1 --sim 0/1')
parser.add_argument('--M', action="store", dest='M', default=4)
parser.add_argument('--N', action="store", dest='N', default=4)
parser.add_argument('--signed', action="store", dest='signed', default=1)
parser.add_argument('--type', action="store", dest='type', default='dadda')
parser.add_argument('--sim', action="store", dest='sim', default=0)
args = parser.parse_args()
M = int(args.M)
N = int(args.N)
sim = int(args.sim)
type = args.type
signed = int(args.signed)

if(signed and N != M):
    print("Signed is not supported when N != M")
    exit()
instance_count = 0

class tree:
    def __init__(self, N, M):
        self.partial_products = [0]*(N+M)
        self.guidance = [0, 0]
    
    def push(self, x):
        self.partial_products[x] += 1
        if self.partial_products[x] > self.guidance[1]:
            self.guidance = [x, self.partial_products[x]]
        return self.partial_products[x] - 1
    
    def set_column(self, column, index):
        self.partial_products[column] = index
        self.update_guidance()
    
    def update_guidance(self):
        self.guidance = [0, 0]
        for i in range(len(self.partial_products)):
            if self.partial_products[i] > self.guidance[1]:
                self.guidance = [i, self.partial_products[i]]
    
    def get_guidance(self):
        return self.guidance
    
    def get_depth(self, column):
        return self.partial_products[column]
    
    def get_partial_products(self):
        return self.partial_products[::-1]
    
    def width(self):
        return len(self.partial_products)

def instance():
    global instance_count
    instance_count += 1
    return instance_count - 1

def AND(output_file, A, B, C):
    output_file.write(f"\twire {C};\n")
    output_file.write(f"\tAND2 instance_{instance()} (.A({A}), .B({B}), .C({C}));\n")

def NAND(output_file, A, B, C):
    output_file.write(f"\twire {C};\n")
    output_file.write(f"\tNAND2 instance_{instance()} (.A({A}), .B({B}), .C({C}));\n")

def HA(output_file, A, B, COUT, SUM):
    output_file.write(f"\twire {COUT}, {SUM};\n")
    output_file.write(f"\tHA instance_{instance()} (.A({A}), .B({B}), .COUT({COUT}), .SUM({SUM}));\n")

def FA(output_file, A, B, CIN, COUT, SUM):
    output_file.write(f"\twire {COUT}, {SUM};\n")
    output_file.write(f"\tFA instance_{instance()} (.A({A}), .B({B}), .CIN({CIN}), .COUT({COUT}), .SUM({SUM}));\n")

def BYPASS(output_file, IN, OUT):
    output_file.write(f"\twire {OUT};\n")
    output_file.write(f"\tassign {OUT} = {IN};\n")

def CONST_ONE(output_file, IN):
    output_file.write(f"\twire {IN} = 1'b1;\n")


def generatePPM(output_file, tree, M, N):
    global signed
    print(signed)
    for i in range(M):
        if(i==M-1 or not signed):
            for j in range(N):
                x = i + j
                y = tree.push(x)
                if(j==N-1 or not signed):
                    AND(output_file, f"a[{i}]", f"b[{j}]", f"level_0__{x}_{y}_")
                else:
                    NAND(output_file, f"a[{i}]", f"b[{j}]", f"level_0__{x}_{y}_")
        else:
            for j in range(N):
                x = i + j
                y = tree.push(x)
                if(j==N-1):
                    NAND(output_file, f"a[{i}]", f"b[{j}]", f"level_0__{x}_{y}_")
                else:
                    AND(output_file, f"a[{i}]", f"b[{j}]", f"level_0__{x}_{y}_")    
    if(signed):
        CONST_ONE(output_file, f"level_0__{N}_{tree.push(N)}_")
        CONST_ONE(output_file, f"level_0__{M+N-1}_{tree.push(M+N-1)}_")
        
   
def header(output_file, N, M):
    output_file.write(f"""
module PPM(a, b, out1, out2);
    
    input [{N-1}:0] a;
    input [{M-1}:0] b;
    output [{N+M-1}:0] out1, out2;
    
""")
    
def endmodule(output_file):
    output_file.write("endmodule\n")

def reduce(output_file, level, tree):
    output_next_row = 0
    for i in range(0, tree.width()):
        input_row = 0
        output_row = output_next_row
        output_next_row = 0 
        while tree.get_depth(i) >= 3:
            FA(output_file, f"level_{level}__{i}_{input_row}_", f"level_{level}__{i}_{input_row+1}_", f"level_{level}__{i}_{input_row+2}_", f"level_{level+1}__{i+1}_{output_next_row}_", f"level_{level+1}__{i}_{output_row}_")
            tree.set_column(i, tree.get_depth(i) - 3)
            input_row += 3
            output_row += 1
            output_next_row += 1
        while tree.get_depth(i) >= 2:
            HA(output_file, f"level_{level}__{i}_{input_row}_", f"level_{level}__{i}_{input_row+1}_", f"level_{level+1}__{i+1}_{output_next_row}_", f"level_{level+1}__{i}_{output_row}_")
            tree.set_column(i, tree.get_depth(i) - 2)
            input_row += 2
            output_row += 1
            output_next_row += 1
        while tree.get_depth(i) >= 1:
            BYPASS(output_file, f"level_{level}__{i}_{input_row}_", f"level_{level+1}__{i}_{output_row}_")
            tree.set_column(i, tree.get_depth(i) - 1)
            input_row +=1
            output_row +=1
        tree.set_column(i, output_row)

def assign_outputs(output_file, level, tree):
    a=[]
    b=[]
    for i in range(tree.width()):
        if(tree.get_depth(i)>0):
            a.append(f"level_{level}__{i}_0_")
        else:
            a.append("1'b0")
        if(tree.get_depth(i)>1):
            b.append(f"level_{level}__{i}_1_")
        else:
            b.append("1'b0")
    output_file.write("\tassign out1={"+", ".join(a[::-1])+"};\n")
    output_file.write("\tassign out2={"+", ".join(b[::-1])+"};\n")

        
PPM_tree = tree(N, M)

PPM=open("PPM.v", 'w')
header(PPM, N, M)
generatePPM(PPM, PPM_tree, N, M)
print(PPM_tree.get_partial_products())
level = 0
while(PPM_tree.get_guidance()[1]>2):
    PPM.write(f"\t//Level {level}\n")
    reduce(PPM, level, PPM_tree)
    level+=1
    print(PPM_tree.get_partial_products())
assign_outputs(PPM,level,PPM_tree)
endmodule(PPM)
PPM.close()
if(signed):
    sign_flag = "-DSIGNED"
else:
    sign_flag = ""
if(sim):
    os.system(f"iverilog PPM.v cells.v PPM_tb.v -DSET_WIDTH -DN={N} -DM={M} {sign_flag}; ./a.out")