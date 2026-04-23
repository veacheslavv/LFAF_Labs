from copy import deepcopy
from itertools import combinations


class Grammar:
    def __init__(self, VN, VT, P, S):
        """
        VN - non-terminals (set of str)
        VT - terminals (set of str)
        P  - productions (dict: str -> list of str)
        S  - start symbol (str)
        """
        self.VN = set(VN)
        self.VT = set(VT)
        self.P = deepcopy(P)
        self.S = S

    def copy(self):
        return Grammar(self.VN, self.VT, self.P, self.S)

    def print_grammar(self, title="Grammar"):
        print(f"\n{'='*50}")
        print(f"  {title}")
        print(f"{'='*50}")
        print(f"  VN = {sorted(self.VN)}")
        print(f"  VT = {sorted(self.VT)}")
        print(f"  S  = {self.S}")
        print(f"  Productions:")
        for lhs in sorted(self.P):
            for rhs in self.P[lhs]:
                print(f"    {lhs} -> {'ε' if rhs == '' else rhs}")
        print()


def find_nullable(P):
    """Find all nullable non-terminals (can derive ε)."""
    nullable = set()
    # direct ε-producers
    for lhs, rules in P.items():
        if '' in rules:
            nullable.add(lhs)
    # propagate
    changed = True
    while changed:
        changed = False
        for lhs, rules in P.items():
            if lhs in nullable:
                continue
            for rhs in rules:
                if all(sym in nullable for sym in rhs):
                    nullable.add(lhs)
                    changed = True
                    break
    return nullable


def step1_eliminate_epsilon(grammar):
    """Step 1: Eliminate ε-productions."""
    g = grammar.copy()
    nullable = find_nullable(g.P)
    print(f"  Nullable symbols: {nullable}")

    new_P = {}
    for lhs, rules in g.P.items():
        new_rules = set()
        for rhs in rules:
            if rhs == '':
                continue  # skip ε directly; add ε for S later if needed
            # generate all combinations where nullable symbols may be omitted
            nullable_positions = [i for i, sym in enumerate(rhs) if sym in nullable]
            for r in range(len(nullable_positions) + 1):
                for positions_to_remove in combinations(nullable_positions, r):
                    new_rhs = ''.join(
                        sym for i, sym in enumerate(rhs)
                        if i not in positions_to_remove
                    )
                    if new_rhs != '':
                        new_rules.add(new_rhs)
        new_P[lhs] = list(new_rules)

    # If start symbol was nullable, add S -> ε
    if g.S in nullable:
        new_P[g.S].append('')

    g.P = new_P
    return g


def step2_eliminate_renamings(grammar):
    """Step 2: Eliminate unit productions (renamings A -> B)."""
    g = grammar.copy()

    def unit_closure(symbol):
        """Find all symbols reachable via unit productions."""
        reachable = {symbol}
        queue = [symbol]
        while queue:
            current = queue.pop()
            for rhs in g.P.get(current, []):
                if len(rhs) == 1 and rhs in g.VN and rhs not in reachable:
                    reachable.add(rhs)
                    queue.append(rhs)
        return reachable

    new_P = {}
    for lhs in g.VN:
        closure = unit_closure(lhs)
        new_rules = set()
        for sym in closure:
            for rhs in g.P.get(sym, []):
                # keep only non-unit rules
                if not (len(rhs) == 1 and rhs in g.VN):
                    new_rules.add(rhs)
        new_P[lhs] = list(new_rules)

    g.P = new_P
    return g


def step3_eliminate_inaccessible(grammar):
    """Step 3: Eliminate inaccessible symbols."""
    g = grammar.copy()
    accessible = {g.S}
    queue = [g.S]
    while queue:
        current = queue.pop()
        for rhs in g.P.get(current, []):
            for sym in rhs:
                if (sym in g.VN or sym in g.VT) and sym not in accessible:
                    accessible.add(sym)
                    if sym in g.VN:
                        queue.append(sym)

    inaccessible = (g.VN | g.VT) - accessible
    print(f"  Inaccessible symbols: {inaccessible if inaccessible else 'none'}")

    g.VN = g.VN & accessible
    g.VT = g.VT & accessible
    g.P = {lhs: rules for lhs, rules in g.P.items() if lhs in accessible}
    return g


def step4_eliminate_nonproductive(grammar):
    """Step 4: Eliminate non-productive symbols."""
    g = grammar.copy()

    # Productive = can derive a terminal string
    productive = set()
    # terminals are productive by definition
    for lhs, rules in g.P.items():
        for rhs in rules:
            if all(sym in g.VT or sym == '' for sym in rhs):
                productive.add(lhs)

    changed = True
    while changed:
        changed = False
        for lhs, rules in g.P.items():
            if lhs in productive:
                continue
            for rhs in rules:
                if all(sym in productive or sym in g.VT for sym in rhs):
                    productive.add(lhs)
                    changed = True
                    break

    nonproductive = g.VN - productive
    print(f"  Non-productive symbols: {nonproductive if nonproductive else 'none'}")

    g.VN = g.VN & productive
    new_P = {}
    for lhs in g.VN:
        new_rules = []
        for rhs in g.P.get(lhs, []):
            if all(sym in productive or sym in g.VT for sym in rhs):
                new_rules.append(rhs)
        if new_rules:
            new_P[lhs] = new_rules
    g.P = new_P
    return g


def step5_to_cnf(grammar):
    """Step 5: Convert to Chomsky Normal Form."""
    g = grammar.copy()
    new_P = {lhs: list(rules) for lhs, rules in g.P.items()}
    counter = [0]

    # Map from terminal -> new non-terminal wrapper
    terminal_map = {}

    def new_nt():
        counter[0] += 1
        name = f"X{counter[0]}"
        return name

    def terminal_nt(term):
        if term not in terminal_map:
            nt = new_nt()
            terminal_map[term] = nt
            g.VN.add(nt)
            new_P[nt] = [term]
        return terminal_map[term]

    # Pass 1: Replace terminals in rules of length >= 2
    for lhs in list(new_P.keys()):
        updated = []
        for rhs in new_P[lhs]:
            if len(rhs) >= 2:
                new_rhs = []
                for sym in rhs:
                    if sym in g.VT:
                        new_rhs.append(terminal_nt(sym))
                    else:
                        new_rhs.append(sym)
                updated.append(''.join(new_rhs))
            else:
                updated.append(rhs)
        new_P[lhs] = updated

    # Pass 2: Break rules of length > 2 into binary rules
    for lhs in list(new_P.keys()):
        updated = []
        for rhs in new_P[lhs]:
            # rhs is a string; each character is a symbol (assumes all NTs are single-char or mapped)
            # We need to parse multi-char NT names - let's work with symbol lists
            syms = tokenize_rhs(rhs, g.VN, g.VT)
            while len(syms) > 2:
                nt = new_nt()
                g.VN.add(nt)
                new_P[nt] = [''.join(syms[-2:])]
                syms = syms[:-2] + [nt]
            updated.append(''.join(syms))
        new_P[lhs] = updated

    g.P = new_P
    return g


def tokenize_rhs(rhs, VN, VT):
    """
    Parse a production RHS string into a list of symbols.
    Handles multi-character non-terminals like X1, X2, etc.
    """
    syms = []
    i = 0
    # Sort VN by length descending to prefer longer matches
    sorted_VN = sorted(VN, key=len, reverse=True)
    while i < len(rhs):
        matched = False
        for nt in sorted_VN:
            if rhs[i:i+len(nt)] == nt:
                syms.append(nt)
                i += len(nt)
                matched = True
                break
        if not matched:
            syms.append(rhs[i])
            i += 1
    return syms


def to_cnf(grammar, verbose=True):
    """Full pipeline: steps 1-5."""
    steps = [
        ("Original Grammar", None),
        ("Step 1: Eliminate ε-productions", step1_eliminate_epsilon),
        ("Step 2: Eliminate unit productions (renamings)", step2_eliminate_renamings),
        ("Step 3: Eliminate inaccessible symbols", step3_eliminate_inaccessible),
        ("Step 4: Eliminate non-productive symbols", step4_eliminate_nonproductive),
        ("Step 5: Chomsky Normal Form", step5_to_cnf),
    ]

    current = grammar
    for title, fn in steps:
        if fn is not None:
            print(f"\n>>> {title}")
            current = fn(current)
        current.print_grammar(title)

    return current


# ── Variant 16 grammar ───────────────────────────────────────────────────────

def build_variant16():
    VN = {'S', 'A', 'B', 'C', 'D'}
    VT = {'a', 'b'}
    P = {
        'S': ['abAB'],          # 1
        'A': ['aSab', 'BS', 'aA', 'b'],   # 2,3,4,5
        'B': ['BA', 'ababB', 'b', ''],    # 6,7,8,9  ('' = ε)
        'C': ['AS'],            # 10
        'D': [],                # not in P explicitly
    }
    # Clean up empty lists
    P = {k: v for k, v in P.items() if v}
    return Grammar(VN, VT, P, 'S')


if __name__ == '__main__':
    print("╔══════════════════════════════════════════════════╗")
    print("║  CNF Converter — Variant 16                      ║")
    print("║  Formal Languages & Finite Automata, FAF-243     ║")
    print("╚══════════════════════════════════════════════════╝")

    g = build_variant16()
    result = to_cnf(g)

    print("\n" + "="*50)
    print("  FINAL CNF GRAMMAR")
    print("="*50)
    result.print_grammar("CNF Result")
