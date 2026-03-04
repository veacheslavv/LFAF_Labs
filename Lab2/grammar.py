class Grammar:
    def __init__(self, VN, VT, P, S):
        self.VN = VN        
        self.VT = VT        
        self.P  = P         
        self.S  = S         

    def classify_chomsky(self):
        is_right_linear = True
        is_left_linear  = True
        is_type2        = True
        is_type1        = True

        for lhs, rhs_list in self.P.items():
            if len(lhs) > 1:
                is_type2        = False
                is_right_linear = False
                is_left_linear  = False
                for rhs in rhs_list:
                    if rhs != 'ε' and len(lhs) > len(rhs):
                        is_type1 = False
            else:
                for rhs in rhs_list:
                    if rhs == 'ε':
                        continue
                    if is_right_linear:
                        ok = (len(rhs) == 1 and rhs in self.VT) or \
                             (len(rhs) == 2 and rhs[0] in self.VT and rhs[1] in self.VN)
                        if not ok:
                            is_right_linear = False
                    if is_left_linear:
                        ok = (len(rhs) == 1 and rhs in self.VT) or \
                             (len(rhs) == 2 and rhs[0] in self.VN and rhs[1] in self.VT)
                        if not ok:
                            is_left_linear = False

        if is_right_linear or is_left_linear:
            return "Type 3 – Regular Grammar"
        elif is_type2:
            return "Type 2 – Context-Free Grammar"
        elif is_type1:
            return "Type 1 – Context-Sensitive Grammar"
        else:
            return "Type 0 – Unrestricted Grammar"

    def __str__(self):
        lines = [f"G = (VN={self.VN}, VT={self.VT}, P, S='{self.S}')"]
        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                lines.append(f"  {lhs} -> {rhs}")
        return "\n".join(lines)
