from random import choices
import math

precision = 4 #desired number of decimal places of precision

#Huffman Encoding

class Source:
    def __init__(self, symbols, probs, normalize = 0):
        #mapping is a dictionary with keys symbols and values the corresponding probabilities
        #can input symbols as list of chars or string, probs as list of numbers
        assert len(symbols) == len(probs), 'Each symbol must correspond to exactly one probability'
        
        self.probs = probs
        if normalize:
            #normalize probabilities to sum to 1
            currsum = sum(probs)
            if round(currsum,precision) != 1.0:
                newprobs = [float(p)/currsum for p in probs]
                self.probs = newprobs               
        else:
            assert round(sum(probs),precision) == 1.0, 'Probabilities must sum to 1'
            
        self.symbols = symbols
        
        self.mapping = dict([(self.symbols[i],self.probs[i]) for i in range(len(self.symbols))])
    
    def print(self):
        print(sorted(self.mapping.items()))
        
    def generate(self):
        return choices(list(self.mapping.keys()), self.probs)[0]
        
    def emit(self, n):
        result = ''
        for i in range(n):
            result += self.generate()
        return result
        
    def entropy(self):
        #returns the entropy of the source
        H = 0
        for p in self.probs:
            H += p*math.log(1.0/p, 2)
        return round(H,precision)

class Encoding:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.mapping = dict([(inputs[i],outputs[i]) for i in range(len(inputs))])
        
    def encode(self, text):
        result = ''
        for item in text:
            result = result + self.mapping[item]
        return result
        
    def print(self):
        print(sorted(self.mapping.items()))
        
class Node:
    def __init__(self, value, items, childL = None, childR = None):
        self.value = value
        self.items = items
        #nodes are binary for this purpose so each can have a left and/or right child
        self.childL = childL
        self.childR = childR
        
    def print(self):
        #mostly for debugging purposes, prints nodes in a more readable manner
        print('[',self.value,', ',self.items,', ','[', self.childL, self.childR, ']]')
        
    def has_child(self):
        if self.childL == None and self.childR == None:
            return False
        return True
        
def step(nodes):
    result_nodes = nodes
    #find the two minimum value nodes and group them as children of a new node
    #find the minimum value node and remove it from the result list
    min_node = min(nodes, key= lambda n:n.value)
    result_nodes.remove(min_node)
    #find the new minimum value node and also remove it from the result list
    min_node_2 = min(result_nodes, key= lambda n:n.value)
    result_nodes.remove(min_node_2)
    #group these two nodes as children of a new node with value = sum of their values, and two min nodes as children
    new_node = Node(min_node.value + min_node_2.value, min_node.items + min_node_2.items, min_node, min_node_2)
    #add this new node to resulting nodes list and return
    result_nodes.append(new_node)
    return result_nodes
    
def encode_tree(tree, encoding_sofar=''):
    #if the node (tree) has no children, return
    if not tree.has_child():
        return [(tree.items, encoding_sofar)] 
    #otherwise recurse along the two branches, encoding a 0 on the left branch and 1 on the right (arbitrarily chosen which 0/1) 
    else:
        treeL = tree.childL
        treeR = tree.childR
        return encode_tree(treeL,encoding_sofar+'0') + encode_tree(treeR,encoding_sofar+'1')
    
        
def huffman(source):
    #creates a Huffman encoding for the given source
    #first create the tree
    nodes = []
    for symbol in source.mapping.keys():
        nodes.append(Node(source.mapping[symbol],(symbol,source.mapping[symbol])))
    while len(nodes) > 1:
        nodes = step(nodes)
    tree=nodes[0]
    #generate encoding from tree
    result = encode_tree(tree)
    inputs = []
    outputs = []
    for item in result:
        inputs.append(item[0][0])
        outputs.append(item[1])    
    huffman = Encoding(inputs, outputs)
    return huffman       
    
def expected_length(source, encoding):
        #returns expected codeword length for the given encoding
        assert len(source.symbols) == len(encoding.inputs), 'Source and encoding lengths are not compatible'
        L = 0
        for item in source.mapping:
            L += (source.mapping[item]*len(encoding.encode(item)))
        return round(L,precision)

#testing Source class:      
#simple_source = Source('01',[.5,.5])
#print(simple_source.emit(10))

lecture_source = Source('WXYZ',[.4,.2,.3,.1])
print('Source:',end = ' '),lecture_source.print()
lecture_result = huffman(lecture_source)
print('Encoding:',end = ' '),lecture_result.print()
print('Entropy of source = ',lecture_source.entropy())
print('Expected codeword length of Huffman encoding = ',expected_length(lecture_source, lecture_result))

print('\n')

livi_source = Source('ABCDE',[3, 2, 1, 1, 1], normalize=1)
print('Source:',end = ' '),livi_source.print()
livi_huffman = huffman(livi_source)
print('Encoding:',end = ' '),livi_huffman.print()
print('Entropy of source = ',livi_source.entropy())
print('Expected codeword length of Huffman encoding = ',expected_length(livi_source, livi_huffman))

print('Example:')
example_text = livi_source.emit(12)
print('Source emits: ',example_text)
example_encoded = livi_huffman.encode(example_text)
print('Huffman encoding is: ',example_encoded,' with average codeword length ',round(len(example_encoded)/len(example_text),precision))
