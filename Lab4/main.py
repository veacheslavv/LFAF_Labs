from regex_parser import parse_regex
from generator import generate_strings

REGEXES = [
    "(S|T)(U|V)W*Y+24",
    "L(M|N)O^3P*Q(2|3)",
    "R*S(T|U|V)W(X|Y|Z)^2"
]

LIMIT = 5  

def main():
    for i, regex in enumerate(REGEXES, 1):
        print(f"\n=== Regex {i}: {regex} ===")

        parsed = parse_regex(regex)
        results = generate_strings(parsed, LIMIT)

        print("Generated strings:")
        for r in results[:20]:  # limit output
            print(r)

if __name__ == "__main__":
    main()
