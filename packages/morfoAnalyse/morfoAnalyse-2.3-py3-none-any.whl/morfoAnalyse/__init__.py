def morfoAnaliz(inputW, root, OT, FEL, SIFAT, RAVISH, SON, OLMOSH):
    root_3 = []

    # Split the input string into words
    words = inputW[0].split()  # Assuming inputW contains a single string as the first element

    for word in words:
        yx = ''
        otstem = felstem = sifatstem = ravishstem = sonstem = olmoshstem = ''

        for x in word: 
            yx += x
            for r in root:
                if yx == r['stem']:
                    if r['turkum'] == 'NOUN':
                        otstem = yx
                    elif r['turkum'] == 'VERB':
                        felstem = yx
                    elif r['turkum'] == 'ADJECTIVE':
                        sifatstem = yx
                    elif r['turkum'] == 'ADVERB':
                        ravishstem = yx
                    elif r['turkum'] == 'NUMBER':
                        sonstem = yx
                    elif r['turkum'] == 'PRONOUN':
                        olmoshstem = yx

        # Extract suffixes
        diffot = word.replace(otstem, "") if otstem else ""
        difffel = word.replace(felstem, "") if felstem else ""
        diffsifat = word.replace(sifatstem, "") if sifatstem else ""
        diffravish = word.replace(ravishstem, "") if ravishstem else ""
        diffson = word.replace(sonstem, "") if sonstem else ""
        diffolmosh = word.replace(olmoshstem, "") if olmoshstem else ""

        # Analyze suffixes
        analizot = findOtSuffix(OT, diffot)
        analizfel = findOtSuffix(FEL, difffel)
        analizsifat = findOtSuffix(SIFAT, diffsifat)
        analizravish = findOtSuffix(RAVISH, diffravish)
        analizson = findOtSuffix(SON, diffson)
        analizolmosh = findOtSuffix(OLMOSH, diffolmosh)

        # Append results
        if otstem:
            root_3.append(f'Input: {word} -> Root word: {otstem} -> Word Class: NOUN -> Suffix: {diffot} -> Analyze: {analizot}')
        if felstem:
            root_3.append(f'Input: {word} -> Root word: {felstem} -> Word Class: VERB -> Suffix: {difffel} -> Analyze: {analizfel}')
        if sifatstem:
            root_3.append(f'Input: {word} -> Root word: {sifatstem} -> Word Class: ADJECTIVE -> Suffix: {diffsifat} -> Analyze: {analizsifat}')
        if ravishstem:
            root_3.append(f'Input: {word} -> Root word: {ravishstem} -> Word Class: ADVERB -> Suffix: {diffravish} -> Analyze: {analizravish}')
        if sonstem:
            root_3.append(f'Input: {word} -> Root word: {sonstem} -> Word Class: NUMBER -> Suffix: {diffson} -> Analyze: {analizson}')
        if olmoshstem:
            root_3.append(f'Input: {word} -> Root word: {olmoshstem} -> Word Class: PRONOUN -> Suffix: {diffolmosh} -> Analyze: {analizolmosh}')

    return root_3        

# Helper functions remain unchanged
def findOtSuffix(suffix, inputsuffix):
    analizot = ''
    go = ''
    model = ''
    analizot1 = ''
    count = 0
    l = list()
    for gword in inputsuffix:
        inputsuffix1 = inputsuffix.replace(analizot1, "")
        if len(inputsuffix) == 0:
            break
        else:   
            analizot1 += AnalizSuffix(suffix, inputsuffix1)
            l.append(AnalizSuffix(suffix, inputsuffix1))
            while '' in l:
                l.remove("")
            count += 1
    for x in l:
        analizot += x + "+"
        for o in suffix:
            if x == o['suffix']:
                model += o['tegi'] + "+"
    return analizot[:-1] + "->Modeli: " + model[:-1]   

def AnalizSuffix(suffix, inputsuffix):
    go = ''
    analizot = ''
    model = ''

    for x in inputsuffix:
        go += x
        for o in suffix:
            if go == o['suffix']: 
                analizot = go
                model = o['tegi']
    return analizot