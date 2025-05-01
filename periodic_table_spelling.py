def find_spellings(word, pos=0, current="", result=None):
    if result is None: result = []
    if pos >= len(word):
        if current: result.append(current.strip())
        return
    # Try one-letter element
    if word[pos].upper() in one_letter:
        find_spellings(word, pos + 1, current + word[pos].upper(), result)
    # Try two-letter element
    if pos + 1 < len(word):
        possible_element = word[pos].upper() + word[pos + 1].lower()
        if possible_element in two_letter:
            find_spellings(word, pos + 2, current + possible_element, result)

# setup periodic table elements
elements = "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og"
one_letter = set()
two_letter = set()
for element in elements.split():
    if len(element) == 1: one_letter.add(element.upper())
    else: two_letter.add(element[0].upper() + element[1].lower())

# find spellings using recursion
result = []
find_spellings(input(), result=result)
print("\n".join(result) if result else "none")
