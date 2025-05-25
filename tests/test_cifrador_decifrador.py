from src.cifrador_decifrador import criptografar_vigenere, descriptografar_vigenere, gerar_keystream

def test_criptografar_vigenere():
    plaintext = "EXEMPLO" # Letra maiúscula sem espaço
    key = "KEY"
    ciphertext_esperado = "OBCWTJY"
    teste_1 = (criptografar_vigenere(plaintext, key) == ciphertext_esperado)

    plaintext = "EXEMPLO EXEMPLO" # Letra maiúscula com espaço
    key = "KEY"
    ciphertext_esperado = "OBCWTJY IVOQNVS"
    teste_2 = (criptografar_vigenere(plaintext, key) == ciphertext_esperado)

    plaintext = "exemplo" # Letra minúscula
    key = "KEY"
    ciphertext_esperado = "OBCWTJY"
    teste_3 = (criptografar_vigenere(plaintext, key) == ciphertext_esperado) # Cifra gerada sempre em upper case
    
    plaintext = (
        "The House of Representatives shall be composed of Members "
        "chosen every second Year by the People of the several States, and the Electors "
        "in each State shall have the Qualifications requisite for "
        "Electors of the most numerous Branch of the State Legislature."

        "No Person shall be a Representative who shall not have attained to the "
        "Age of twenty five Years, and been seven Years a Citizen of the United States, "
        "and who shall not, when elected, be an Inhabitant of that State in which he shall be chosen."

        "Representatives and direct Taxes shall be apportioned among the several States "
        "which may be included within this Union, according to their "
        "respective Numbers, which shall be determined by adding to the whole Number "
        "of free Persons, including those bound to Service for a Term of Years, "
        "and excluding Indians not taxed, three fifths of all other Persons. "
        "The actual Enumeration shall be made within three Years after the first "
        "Meeting of the Congress of the United States, and within every subsequent "
        "Term of ten Years, in such Manner as they shall by Law direct.The Number of Representatives "
        "shall not exceed one for every thirty Thousand, but each State shall have at Least one Representative; "
        "and until such enumeration shall be made, the State of New Hampshire shall "
        "be entitled to chuse three, Massachusetts eight, Rhode-Island and Providence Plantations one, "
        "Connecticut five, New-York six, New Jersey four, Pennsylvania eight, "
        "Delaware one, Maryland six, Virginia ten, North Carolina five, South Carolina five, and Georgia three."

        "When vacancies happen in the Representation from any State, "
        "the Executive Authority thereof shall issue Writs of Election to fill such Vacancies."

        "The House of Representatives shall chuse their Speaker and other Officers;"
        "and shall have the sole Power of Impeachment."
    ) # String extensa, sem acentos
    key = "CRYPTANALYSIS"
    ciphertext_esperado = (
        "VYC WHUFE ZD JMHTVQTGTNTTTWA KJRJA UE POXNGAWF FD BXMOECQ "
        "UPGUVL TOEEY DCUWFF PCPK BL TSC HMGRCC DY TUE DCNMJCC QITTRS, LLV BZG VJTVTBRD "
        "GF MSEY QITTR SSYDT ZCMC IAE DULJANAERRXHNF RPOMQKKKC UHR "
        "RLPALWJU FD IAE ZODR FCEGIMJL BEAYAZ WX VYC HMAGE WCYQKNRRJKE."

        "AO ACJAGP JFPEL OE L PWXJGJCCMAGIGC OPG UYYAE NBT SYNM SVKYXGEQ TZ RZM "
        "SIV MU MWRNEW XQNG PCPKS, NNO ZWMF UVTTG YRACQ S KAVZXTG OS TSC MVAVVB HMAGED, "
        "YFL OJF QWTLY NZR, OPWP VJTVTRD, MC SV APYYQBTNNE MX BZCK QITTR IY UZQUJ YC HAAYL MC UPGUVL."

        "GXPEEDCFBSVZTTL AAD OGJMUV KYMXS FHLJD JW CGNDKTVOYCV IEQEE IAE FEGCJID UKYIXS "
        "JHTAZ USA SC XGCYUOCV EAVYGC MHVS FLAWF, CTADKDVNR RG BZGZP "
        "GXSCENRADW PLKQXRF, WSGUP KJRJA UE QEECJUAPVB QR AQDTLY BG VYC LAOYE YSEJWT "
        "FD UKER PPPKWFU, ZLREUQIYE LPGUV ZDNNQ TZ QWZNKTC UHR N TPPE WX AVYGL, "
        "AAD PVUTMFZLV BNQILLK VGV KYMXD, GHCCW NAHKFH HF NLW MLPWT GCGLOAS. "
        "EFW IUVLYA XNHMPPSBAQE QWTLY BP KSLW YZRWBN GHCCW GWCIQ PYTRR EFW NATJR "
        "BXEGIYE GN LJV ADGGEEDQ GN LJV SCBTRD DRSBWU, RLS PIGHTL WDWTP QJUSRQFCFB "
        "LGIK DY TRN JCSZK, KE QJVH ZAYLWZ SU KFTR SUAWJ TG DCN BXKEPT.EFW VMOSCG HF EEAPWAWPKYIBVRS "
        "DFSTD PFR TQCREO MFM XQI CKXRL TSGJBQ VYMJLAAD, MSL MSEY QITTR SSYDT ZCMC PM LRADR GVW TVNGXSRNEYLQNG; "
        "RLS NNGIW QMKZ GESBXRNTTMF AZCCJ QX MNDP, RZM KVRRT HF AEH FSUHUYGGX SUAWJ "
        "TM WPKGIEEQ TZ AZCKG KFGXE, ZADQSKZWJCIMS RIRFL, ZZQUC-XLLNNO YFL HTFTXWEACP NDIFVRRXHNF OYC, "
        "UWFPVAIBCHT QGNM, FGN-WDKK FII, LWE BGIQTR FBUC, NWVFUPJKTNVA PGYPL, "
        "FVJPPAEE ZLW, USTPJPGD FII, TAZYKEGP MEA, NZPLP UCIMABNN FTTW, AGWKF RTRBLTLS NAXV, YCW GROCEAI LJICT."

        "PHRN GYUIFEZCH AACPPL AV LJV PTIRRSPLLILKFL UKOZ AYW KBSVV, "
        "RWX EKENSLQNG RSIAOEIEW LPWTVMU LHNLW GKAMG NPXMS BF PJWKLKFL IH FVLW QMKZ XRAPGCVED."

        "RZM ZQLQT HF EEAPWAWPKYIBVRS DFSTD EYSHX TUETP KXWCBCG TNQ OEFWZ GHWGRXRF;"
        "AYB KPSNC FPOE GHP QGTW RFUTK OS IXNWIUJDCCM."
    ) # Mantém pontuações, hífens e espaços
    teste_4 = (criptografar_vigenere(plaintext, key)) == ciphertext_esperado

    assert (teste_1 and teste_2 and teste_3 and teste_4)


def test_descriptografar_vigenere():
    ciphertext = "OBCWTJY" # Letra maiúscula sem espaço
    key = "KEY"
    plaintext_esperado = "EXEMPLO"
    teste_1 = (descriptografar_vigenere(ciphertext, key) == plaintext_esperado)

    ciphertext = "OBCWTJY IVOQNVS" # Letra maiúscula com espaço
    key = "KEY"
    plaintext_esperado = "EXEMPLO EXEMPLO"
    teste_2 = (descriptografar_vigenere(ciphertext, key) == plaintext_esperado)

    ciphertext = "obcwtjy" # Letra minúscula
    key = "KEY"
    plaintext_esperado = "EXEMPLO" # Plaintext gerado sempre em upper case
    teste_3 = (descriptografar_vigenere(ciphertext, key) == plaintext_esperado)

    ciphertext = (
        "VYC WHUFE ZD JMHTVQTGTNTTTWA KJRJA UE POXNGAWF FD BXMOECQ "
        "UPGUVL TOEEY DCUWFF PCPK BL TSC HMGRCC DY TUE DCNMJCC QITTRS, LLV BZG VJTVTBRD "
        "GF MSEY QITTR SSYDT ZCMC IAE DULJANAERRXHNF RPOMQKKKC UHR "
        "RLPALWJU FD IAE ZODR FCEGIMJL BEAYAZ WX VYC HMAGE WCYQKNRRJKE."

        "AO ACJAGP JFPEL OE L PWXJGJCCMAGIGC OPG UYYAE NBT SYNM SVKYXGEQ TZ RZM "
        "SIV MU MWRNEW XQNG PCPKS, NNO ZWMF UVTTG YRACQ S KAVZXTG OS TSC MVAVVB HMAGED, "
        "YFL OJF QWTLY NZR, OPWP VJTVTRD, MC SV APYYQBTNNE MX BZCK QITTR IY UZQUJ YC HAAYL MC UPGUVL."

        "GXPEEDCFBSVZTTL AAD OGJMUV KYMXS FHLJD JW CGNDKTVOYCV IEQEE IAE FEGCJID UKYIXS "
        "JHTAZ USA SC XGCYUOCV EAVYGC MHVS FLAWF, CTADKDVNR RG BZGZP "
        "GXSCENRADW PLKQXRF, WSGUP KJRJA UE QEECJUAPVB QR AQDTLY BG VYC LAOYE YSEJWT "
        "FD UKER PPPKWFU, ZLREUQIYE LPGUV ZDNNQ TZ QWZNKTC UHR N TPPE WX AVYGL, "
        "AAD PVUTMFZLV BNQILLK VGV KYMXD, GHCCW NAHKFH HF NLW MLPWT GCGLOAS. "
        "EFW IUVLYA XNHMPPSBAQE QWTLY BP KSLW YZRWBN GHCCW GWCIQ PYTRR EFW NATJR "
        "BXEGIYE GN LJV ADGGEEDQ GN LJV SCBTRD DRSBWU, RLS PIGHTL WDWTP QJUSRQFCFB "
        "LGIK DY TRN JCSZK, KE QJVH ZAYLWZ SU KFTR SUAWJ TG DCN BXKEPT.EFW VMOSCG HF EEAPWAWPKYIBVRS "
        "DFSTD PFR TQCREO MFM XQI CKXRL TSGJBQ VYMJLAAD, MSL MSEY QITTR SSYDT ZCMC PM LRADR GVW TVNGXSRNEYLQNG; "
        "RLS NNGIW QMKZ GESBXRNTTMF AZCCJ QX MNDP, RZM KVRRT HF AEH FSUHUYGGX SUAWJ "
        "TM WPKGIEEQ TZ AZCKG KFGXE, ZADQSKZWJCIMS RIRFL, ZZQUC-XLLNNO YFL HTFTXWEACP NDIFVRRXHNF OYC, "
        "UWFPVAIBCHT QGNM, FGN-WDKK FII, LWE BGIQTR FBUC, NWVFUPJKTNVA PGYPL, "
        "FVJPPAEE ZLW, USTPJPGD FII, TAZYKEGP MEA, NZPLP UCIMABNN FTTW, AGWKF RTRBLTLS NAXV, YCW GROCEAI LJICT."

        "PHRN GYUIFEZCH AACPPL AV LJV PTIRRSPLLILKFL UKOZ AYW KBSVV, "
        "RWX EKENSLQNG RSIAOEIEW LPWTVMU LHNLW GKAMG NPXMS BF PJWKLKFL IH FVLW QMKZ XRAPGCVED."

        "RZM ZQLQT HF EEAPWAWPKYIBVRS DFSTD EYSHX TUETP KXWCBCG TNQ OEFWZ GHWGRXRF;"
        "AYB KPSNC FPOE GHP QGTW RFUTK OS IXNWIUJDCCM."
    ) # String extensa, sem acentos
    key = "CRYPTANALYSIS"
    plaintext_esperado = (
        "The House of Representatives shall be composed of Members "
        "chosen every second Year by the People of the several States, and the Electors "
        "in each State shall have the Qualifications requisite for "
        "Electors of the most numerous Branch of the State Legislature."

        "No Person shall be a Representative who shall not have attained to the "
        "Age of twenty five Years, and been seven Years a Citizen of the United States, "
        "and who shall not, when elected, be an Inhabitant of that State in which he shall be chosen."

        "Representatives and direct Taxes shall be apportioned among the several States "
        "which may be included within this Union, according to their "
        "respective Numbers, which shall be determined by adding to the whole Number "
        "of free Persons, including those bound to Service for a Term of Years, "
        "and excluding Indians not taxed, three fifths of all other Persons. "
        "The actual Enumeration shall be made within three Years after the first "
        "Meeting of the Congress of the United States, and within every subsequent "
        "Term of ten Years, in such Manner as they shall by Law direct.The Number of Representatives "
        "shall not exceed one for every thirty Thousand, but each State shall have at Least one Representative; "
        "and until such enumeration shall be made, the State of New Hampshire shall "
        "be entitled to chuse three, Massachusetts eight, Rhode-Island and Providence Plantations one, "
        "Connecticut five, New-York six, New Jersey four, Pennsylvania eight, "
        "Delaware one, Maryland six, Virginia ten, North Carolina five, South Carolina five, and Georgia three."

        "When vacancies happen in the Representation from any State, "
        "the Executive Authority thereof shall issue Writs of Election to fill such Vacancies."

        "The House of Representatives shall chuse their Speaker and other Officers;"
        "and shall have the sole Power of Impeachment."
    ).upper() # O resultado é em maiúsculo, por isso a capitalização
    teste_4 = (descriptografar_vigenere(ciphertext, key)) == plaintext_esperado

    assert (teste_1 and teste_2 and teste_3 and teste_4)


def test_gerar_keystream():
    plaintext = "EXEMPLO" # Sem espaço
    key = "KEY"
    keystream_esperado = "KEYKEYK"
    teste_1 = (gerar_keystream(plaintext, key) == keystream_esperado)

    plaintext = "EXEMPLO EXEMPLO EXEMPLO" # Com espaço
    key = "KEY"
    keystream_esperado = "KEYKEYK EYKEYKE YKEYKEY"
    teste_2 = (gerar_keystream(plaintext, key) == keystream_esperado)

    plaintext = "EXEMPLO, EXEMPLO! EXEMPLO-EXEMPLO; 'EXEMPLO'." # Com caracteres não-letras
    key = "KEY"
    keystream_esperado = "KEYKEYK  EYKEYKE  YKEYKEY KEYKEYK   EYKEYKE  "
    teste_3 = (gerar_keystream(plaintext, key) == keystream_esperado)

    assert (teste_1 and teste_2 and teste_3)
