import os

instance_count = 0

class tree:
    def __init__(self, N, M):
        self.partial_products = [0]*(N+M)
        self.guide = 0
    def push(self, x):
        self.partial_products[x]+=1
        self.guide = max(self.partial_products[x], self.guide)
        return self.partial_products[x]-1
    def get_partial_products(self):
        return self.partial_products[::-1]


def instance():
    global instance_count
    instance_count+=1
    return instance_count-1

def AND(output_file, A, B, C):
    output_file.write(f"\tAND2 instance_{instance()} (.A({A}), .B({B}), .C({C}));\n")

def HA(output_file, A, B, COUT, SUM):
    output_file.write(f"\tHA instance_{instance()} (.A({A}), .B({B}), .COUT({COUT}), .SUM({SUM}));\n")

def FA(output_file, A, B, CIN, COUT, SUM):
    output_file.write(f"\tFA {instance()} (.A({A}), .B({B}), .CIN({CIN}), .COUT({COUT}), .SUM({SUM}));\n")

def generatePPM(output_file, tree, N, M):
    for i in range(N):
        for j in range(M):
            x = i+j
            y = tree.push(x)
            AND(output_file, f"A[{i}]", f"B[{j}]", f"level_0_{x}_{y}_")

def header(output_file, N, M):
    output_file.write(f"""
module PPM(A, B, OUT1, OUT2);
    
    input [{N-1}:0] A;
    output [{M-1}:0] B;
    output [{N+M-1}:0] OUT1, OUT2;
    
""")
    
def endmodule(output_file):
    output_file.write("endmodule\n")

#def reduce(output_file, level, tree):
#    for i in range(tree):

N, M=4, 4
PPM_tree = tree(N, M)

PPM=open("PPM.v", 'w')
header(PPM, 4, 4)
generatePPM(PPM, PPM_tree, 4, 4)
endmodule(PPM)
print(PPM_tree.get_partial_products())
print(PPM_tree.guide)