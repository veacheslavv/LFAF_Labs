import random
from typing import Dict, List, Set


class Grammar:
    """
    Grammar class for Variant 16
    VN={S, A, B}
    VT={a, b, c, d}
    P={ 
        S → bS     
        S → dA    
        A → aA   
        A → dB    
        B → cB  
        A → b   
        B → a
    }
    """
    
    def __init__(self):
        self.VN: Set[str] = {'S', 'A', 'B'}
        
        self.VT: Set[str] = {'a', 'b', 'c', 'd'}
        
        self.S: str = 'S'
        
        self.P: Dict[str, List[str]] = {
            'S': ['bS', 'dA'],
            'A': ['aA', 'dB', 'b'],
            'B': ['cB', 'a']
        }
    
    def generate_string(self) -> str:

        current = self.S
        max_iterations = 100
        iterations = 0
        
        while iterations < max_iterations:
            temp = ""
            has_non_terminal = False
            
            for symbol in current:
                if symbol in self.VN:
                    has_non_terminal = True
                    if symbol in self.P:
                        production = random.choice(self.P[symbol])
                        temp += production
                else:
                    temp += symbol
            
            current = temp
            
            if not has_non_terminal:
                return current
            
            iterations += 1
        
        return current
    
    def to_finite_automaton(self):

        from finite_automaton import FiniteAutomaton
        
        states = set(self.VN)
        states.add('X')  
        
        alphabet = set(self.VT)
        
        transitions: Dict[str, Dict[str, str]] = {}
        
        for left_side, productions in self.P.items():
            if left_side not in transitions:
                transitions[left_side] = {}
            
            for production in productions:
                if len(production) == 1:
                    transitions[left_side][production] = 'X'
                elif len(production) == 2:
                    terminal = production[0]
                    non_terminal = production[1]
                    transitions[left_side][terminal] = non_terminal
        
        initial_state = self.S
        final_states = {'X'}
        
        return FiniteAutomaton(states, alphabet, transitions, initial_state, final_states)
    
    def __str__(self) -> str:
        """String representation of the grammar"""
        result = "Grammar:\n"
        result += f"V_N = {self.VN}\n"
        result += f"V_T = {self.VT}\n"
        result += f"S = {self.S}\n"
        result += "P = {\n"
        for left_side, productions in self.P.items():
            for production in productions:
                result += f"    {left_side} → {production}\n"
        result += "}"
        return result
