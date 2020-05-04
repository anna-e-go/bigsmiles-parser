# take in smiles string, make a molecular graph 
# need to add in surpressed H?
# convert to CDXML

"""
atoms that don't have brackets are organic subset, have no formal
charge, expected valence H, normal isotopes, not chiral centers
ammonium = [NH+4] = [NH++++]

unless stated, aliphatic bonds are single, can be written with "-"
double bond =
triple bond #
quadruple bond $
aromatic bond and half :
single bonds next to double bonds \ and / (indicate stereochem)

"""

import networkx as nx
from pyparsing import Literal, Word, White, alphas, nestedExpr, quotedString, cStyleComment, alphanums, nums, StringStart, StringEnd



class SmilesGraph:
    def __init__(self):
        self.graph.clear()
        
    graph = nx.Graph()
    parsed_list = []


class SmilesString:
    def __init__(self, input_str):
        self.smiles_string = input_str
    
    smiles_string = ""
    parsed_list = []
    nodes = []

    xml_file = ""

    elements = {"H": "1", "C": "6", "N": "7", "O": "8"}

    _bond = Word('-=#:\/()', exact=1)
    _element_symbols = Literal('He') | Literal('Li') | Literal('Be') | Literal('Ne') | Literal('Na') | Literal('Mg') \
                    | Literal('Al') | Literal('Si') | Literal('Cl') | Literal('Ar') | Literal('Ca') | Literal('Sc') \
                    | Literal('Ti') | Literal('Cr') | Literal('Mn') | Literal('Fe') | Literal('Co') | Literal('Ni') \
                    | Literal('Cu') | Literal('Zn') | Literal('Ga') | Literal('Ge') | Literal('As') | Literal('Se') \
                    | Literal('Br') | Literal('Kr') | Literal('Rb') | Literal('Sr') | Literal('Zr') | Literal('Nb') \
                    | Literal('Mo') | Literal('Tc') | Literal('Ru') | Literal('Rh') | Literal('Pd') | Literal('Ag') \
                    | Literal('Cd') | Literal('In') | Literal('Sn') | Literal('Sb') | Literal('Te') | Literal('Xe') \
                    | Literal('Cs') | Literal('Ba') | Literal('Hf') | Literal('Ta') | Literal('Re') | Literal('Os') \
                    | Literal('Ir') | Literal('Pt') | Literal('Au') | Literal('Hg') | Literal('Tl') | Literal('Pb') \
                    | Literal('Bi') | Literal('Po') | Literal('At') | Literal('Rn') | Literal('Fr') | Literal('Ra') \
                    | Literal('Rf') | Literal('Db') | Literal('Sg') | Literal('Bh') | Literal('Hs') | Literal('Mt') \
                    | Literal('Ds') | Literal('Rg') | Literal('La') | Literal('Ce') | Literal('Pr') | Literal('Nd') \
                    | Literal('Pm') | Literal('Sm') | Literal('Eu') | Literal('Gd') | Literal('Tb') | Literal('Dy') \
                    | Literal('Ho') | Literal('Er') | Literal('Tm') | Literal('Yb') | Literal('Lu') | Literal('Ac') \
                    | Literal('Th') | Literal('Pa') | Literal('Np') | Literal('Pu') | Literal('Am') | Literal('Cm') \
                    | Literal('Bk') | Literal('Cf') | Literal('Es') | Literal('Fm') | Literal('Md') | Literal('No') \
                    | Literal('Lr') \
                    | Literal('H') | Literal('B') | Literal('C') | Literal('N') | Literal('O') | Literal('F') | Literal('P')  \
                    | Literal('S') | Literal('K') | Literal('V') | Literal('Y') | Literal('I') | Literal('W') | Literal('U')
    _aromatic_symbols = Literal('se') | Literal('as') | Word('cnops',exact=1) 
    _symbols = _element_symbols | _aromatic_symbols | Literal('*') | _bond

    
    def parse_to_list(self):
        scanner = self._symbols.scanString(self.smiles_string)
        self.parsed_list = [elem[0][0] for elem in scanner]

    
    def add_bonds_to_list(self):
        print(self.parsed_list)
        i = 0
        while i < len(self.parsed_list)-1:
            curr = self.parsed_list[i]
            nxt = self.parsed_list[i+1]
            if curr in '-=#:\/()':
                i += 1
                continue
            if nxt not in '-=#:\/()':
                self.parsed_list.insert(i+1, '-')
            i += 1
        

    def branch(self):
        open_paren = []
        closed_paren = []
        for i in range(len(self.parsed_list)):
            if self.parsed_list[i] == "(":
                open_paren.append(i)
            if self.parsed_list[i] == ")":
                closed_paren.append(i)
        
        left = self.parsed_list[:min(open_paren)]
        right = self.parsed_list[max(closed_paren)+1:]
        print(left)
        print(right)
        # node_list = self.make_nodes(window, 1)
        # print(node_list)


    def make_nodes(self, atom_bond_list, count):
        node_list = []
        for i in range(len(atom_bond_list)):
            val = atom_bond_list[i]
            temp_dict = {}
            if val in '-=#:\/':
                temp_dict['type'] = 'bond'
            else:
                temp_dict['type'] = 'atom'
            temp_dict['id'] = count
            temp_dict['value'] = val 
            temp_dict['start'] = count - 1
            temp_dict['end'] = count + 1
            node_list.append(temp_dict)
        return node_list


    def list_to_tuples(self):
        if "(" in self.parsed_list and ")" in self.parsed_list:
            self.branch()
        for i in range(len(self.parsed_list)):
            val = self.parsed_list[i]
            temp_dict = {}
            if val in '-=#:\/':
                temp_dict['type'] = 'bond'
            else:
                temp_dict['type'] = 'atom'
            temp_dict['position'] = i
            temp_dict['value'] = val 
            temp_dict['start'] = i - 1
            temp_dict['end'] = i + 1
                
            self.nodes.append(temp_dict)
        # print(self.nodes)


    def generate_xml_top(self, file_name):
        try:
            f = open(file_name + ".cdxml", "w")
            f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
            f.write('<!DOCTYPE CDXML SYSTEM "http://www.cambridgesoft.com/xml/cdxml.dtd" >\n')
            f.write('<CDXML\n>') 
            f.write('<page\n>')
            f.write('<fragment\n>')
            self.xml_file = file_name + ".cdxml"
        except Exception as e:
            print(e)
        

    def fill_in_xml(self):
        up = True
        start_x = 100
        start_y = 200
        f = open(self.xml_file, "a")
        for node in self.nodes:
            print(node)
            if node['type'] == 'atom':
                f.write(self.write_n(node, str(start_x), str(start_y)))
                start_x += 26
                if up:
                    start_y -= 15
                    up = False
                else:
                    start_y += 15
            if node['type'] == 'bond':
                f.write(self.write_b(node, node['position']-1, node['position']+1))

    
    def write_n(self, node_dict, x, y):
        quote = '\"'
        n = "<n\n"
        unique_id = quote + str(node_dict['position']) + quote
        element = quote + self.elements[node_dict['value']] + quote
        position = quote + " ".join([x,y]) + quote 
        return "".join([n, "id=", unique_id, "\nElement=", element, "\np=", position, "\n/>"])

    def write_b(self, node_dict, beginning, end):
        quote = '\"'
        b = "<b\n"
        unique_id = quote + str(node_dict['position']) + quote
        order = "1"
        bond_type = node_dict['value']
        if bond_type == "=":
            order = "2"
        return "".join([b, "id=", unique_id, "\nB=", quote, str(beginning), quote, "\nE=", quote, str(end), quote, "\nOrder=", quote, order, quote, "\n/>"])


    def generate_xml_bottom(self):
        try:
            f = open(self.xml_file, "a")
            f.write('</fragment></page></CDXML>\n') # close fragment
        except Exception as e:
            print(e)



if __name__ == "__main__":
    # test = SmilesString(input_str="C=C")
    # test.parse_to_list()
    # test.list_to_tuples()
    # test.generate_xml_top("demo")
    # test.fill_in_xml()
    # test.generate_xml_bottom()

    # threonine CC(C(C(=O)O)N)O

    test2 = SmilesString(input_str="CC(C(C(=O)O)N)O")
    test2.parse_to_list()
    test2.add_bonds_to_list()
    test2.branch()
