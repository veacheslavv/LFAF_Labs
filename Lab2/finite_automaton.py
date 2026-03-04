from grammar import Grammar

class FiniteAutomaton:
    def __init__(self, Q, sigma, delta, q0, F):
        self.Q     = Q
        self.sigma = sigma
        self.delta = delta   
        self.q0    = q0
        self.F     = F

    def to_regular_grammar(self):
        VN = set(self.Q)
        VT = set(self.sigma)
        S  = self.q0
        P  = {state: [] for state in self.Q}

        for (state, symbol), targets in self.delta.items():
            for target in targets:
                P[state].append(f"{symbol}{target}")   
                if target in self.F:
                    P[state].append(f"{symbol}")        

        return Grammar(VN, VT, P, S)

    def is_deterministic(self):
        """Return True iff every (state, symbol) maps to exactly one state."""
        for (state, symbol), targets in self.delta.items():
            if len(targets) != 1:
                return False
        return True

    def to_dfa(self):
        """
        Subset (powerset) construction.
        Returns a new FiniteAutomaton that is deterministic.
        """
        from collections import deque

        start = frozenset([self.q0])
        dfa_states   = {start}
        dfa_delta    = {}
        queue        = deque([start])
        dfa_final    = set()

        def name(fs):
            return "{" + ",".join(sorted(fs)) + "}"

        while queue:
            current = queue.popleft()
            for symbol in self.sigma:
                reached = set()
                for state in current:
                    for target in self.delta.get((state, symbol), []):
                        reached.add(target)
                if not reached:
                    continue
                reached_fs = frozenset(reached)
                dfa_delta[(name(current), symbol)] = [name(reached_fs)]
                if reached_fs not in dfa_states:
                    dfa_states.add(reached_fs)
                    queue.append(reached_fs)

        for ds in dfa_states:
            if ds & self.F:
                dfa_final.add(name(ds))

        dfa_Q     = {name(ds) for ds in dfa_states}
        dfa_start = name(start)

        return FiniteAutomaton(dfa_Q, self.sigma, dfa_delta, dfa_start, dfa_final)


    def to_dot(self, title="FA"):
        lines = [f'digraph {title} {{', '  rankdir=LR;']
        for f in self.F:
            lines.append(f'  "{f}" [shape=doublecircle];')
        lines.append(f'  "__start__" [shape=point];')
        lines.append(f'  "__start__" -> "{self.q0}";')
        for (state, symbol), targets in self.delta.items():
            for t in targets:
                lines.append(f'  "{state}" -> "{t}" [label="{symbol}"];')
        lines.append("}")
        return "\n".join(lines)

    def __str__(self):
        lines = [f"FA = (Q={self.Q}, Σ={self.sigma}, δ, q0='{self.q0}', F={self.F})"]
        lines.append("Transitions:")
        for (s, sym), targets in sorted(self.delta.items()):
            lines.append(f"  δ({s}, {sym}) = {targets}")
        return "\n".join(lines)
