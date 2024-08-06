import os

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
    output_file.write(f"\tAND2 instance_{instance()} (.A({A}), .B({B}), .C({C}));\n")

def HA(output_file, A, B, COUT, SUM):
    output_file.write(f"\tHA instance_{instance()} (.A({A}), .B({B}), .COUT({COUT}), .SUM({SUM}));\n")

def FA(output_file, A, B, CIN, COUT, SUM):
    output_file.write(f"\tFA instance_{instance()} (.A({A}), .B({B}), .CIN({CIN}), .COUT({COUT}), .SUM({SUM}));\n")

def BYPASS(output_file, IN, OUT):
    output_file.write(f"\tassign {OUT} = {IN};\n")

def generatePPM(output_file, tree, N, M):
    for i in range(N):
        for j in range(M):
            x = i + j
            y = tree.push(x)
            AND(output_file, f"A[{i}]", f"B[{j}]", f"level_0_{x}_{y}_")

def header(output_file, N, M):
    output_file.write(f"""
module PPM(A, B, OUT1, OUT2);
    
    input [{N-1}:0] A;
    input [{M-1}:0] B;
    output [{N+M-1}:0] OUT1, OUT2;
    
""")
    
def endmodule(output_file):
    output_file.write("endmodule\n")

def reduce(output_file, level, tree):
    for i in range(tree.width()):
        j, k = 0, 0
        while tree.get_depth(i) > 3:
            print("FA")
            FA(output_file, f"level_{level}_{i}_{j}_", f"level_{level}_{i}_{j+1}_", f"level_{level}_{i}_{j+2}_", f"level_{level+1}_{i+1}_{k}_", f"level_{level+1}_{i}_{k+1}_")
            tree.set_column(i, tree.get_depth(i) - 3)
            k += 2
            j += 3
        while tree.get_depth(i) > 2:
            print("HA")
            HA(output_file, f"level_{level}_{i}_{j}_", f"level_{level}_{i}_{j+1}_", f"level_{level+1}_{i+1}_{k}_", f"level_{level+1}_{i}_{k+1}_")
            tree.set_column(i, tree.get_depth(i) - 2)
            k += 2
            j += 2
        while tree.get_depth(i) > 1:
            print("BYPASS")
            BYPASS(output_file, f"level_{level}_{i}_{j}_", f"level_{level+1}_{i}_{k}_")
            tree.set_column(i, tree.get_depth(i) - 1)
            k += 1
            j += 1
        tree.set_column(i, k+k_prev)
N, M=4, 4
PPM_tree = tree(N, M)

PPM=open("PPM.v", 'w')
header(PPM, N, M)
generatePPM(PPM, PPM_tree, N, M)

level = 0
while(PPM_tree.get_guidance()[1]>2):
    print("Enteing Reduce")
    reduce(PPM, level, PPM_tree)
    level+=1
endmodule(PPM)
print(PPM_tree.get_partial_products())
print(PPM_tree.get_guidance())