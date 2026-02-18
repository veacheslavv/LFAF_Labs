

from grammar import Grammar
from finite_automaton import FiniteAutomaton


def main():
    print("=" * 60)
    print("FORMAL LANGUAGES & FINITE AUTOMATA - Laboratory Work 1")
    print("Variant 16")
    print("=" * 60)
    print()
    
    grammar = Grammar()
    
    print(grammar)
    print()
    print("=" * 60)
    
    print("\nTask 3b: Generating 5 valid strings from the grammar:")
    print("-" * 60)
    for i in range(1, 6):
        generated_string = grammar.generate_string()
        print(f"{i}. {generated_string}")
    print()
    print("=" * 60)
    
    print("\nTask 3c: Converting Grammar to Finite Automaton:")
    print("-" * 60)
    fa = grammar.to_finite_automaton()
    print(fa)
    print("=" * 60)
    
    print("\nTask 3d: Testing if strings belong to the language:")
    print("-" * 60)
    
    test_strings = [
        "bdab",           # V: S→bS, S→dA, A→aA, A→b
        "bbbdab",         # V: S→bS, S→bS, S→bS, S→dA, A→aA, A→b
        "dab",            # V: S→dA, A→aA, A→b
        "daab",           # V: S→dA, A→aA, A→aA, A→b
        "db",             # V: S→dA, A→b
        "bdca",           # V: S→bS, S→dA, A→dB, B→cB, B→a
        "ddcca",          # V: S→dA, A→dB, B→cB, B→cB, B→a
        "abc",            # Inv: doesn't match grammar
        "d",              # Inv: incomplete
        "da",             # Inv: A cannot go directly to a
        "bda",            # Inv: ends with a without proper path
    ]
    
    for test_string in test_strings:
        belongs = fa.string_belong_to_language(test_string)
        status = "ACCEPTED" if belongs else "REJECTED"
        print(f"'{test_string}' -> {status}")
    


if __name__ == "__main__":
    main()
