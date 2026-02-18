from typing import Dict, Set


class FiniteAutomaton:

    
    def __init__(self, 
                 states: Set[str],
                 alphabet: Set[str],
                 transitions: Dict[str, Dict[str, str]],
                 initial_state: str,
                 final_states: Set[str]):

        self.Q = set(states)
        self.Sigma = set(alphabet)
        self.delta = {k: dict(v) for k, v in transitions.items()}
        self.q0 = initial_state
        self.F = set(final_states)
    
    def string_belong_to_language(self, input_string: str) -> bool:

        current_state = self.q0
        
        for symbol in input_string:
            if symbol not in self.Sigma:
                return False  
            
            if current_state not in self.delta or symbol not in self.delta[current_state]:
                return False  
            
            current_state = self.delta[current_state][symbol]
        
        return current_state in self.F
    
    def __str__(self) -> str:
        result = "Finite Automaton:\n"
        result += f"Q = {self.Q}\n"
        result += f"Σ = {self.Sigma}\n"
        result += f"q0 = {self.q0}\n"
        result += f"F = {self.F}\n"
        result += "δ (transitions):\n"
        
        for state, transitions in sorted(self.delta.items()):
            for symbol, next_state in sorted(transitions.items()):
                result += f"    δ({state}, {symbol}) = {next_state}\n"
        
        return result
