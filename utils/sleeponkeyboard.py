# ENG to THAI

dict_th = ['ๅ','/','-','ภ','ถ','ุ','ึ','ค','ต','จ','ข','ช',
            'ๆ','ไ','ำ','พ','ะ','ั','ี','ร','น','ย','บ','ล','ฃ',
            'ฟ','ห','ก','ด','เ','้','่','า','ส','ว','ง',
            'ผ','ป','แ','อ','ิ','ื','ท','ม','ใ','ฝ',
            '+','๑','๒','๓','๔','ู','฿','๕','๖','๗','๘','๙',
            '๐','"','ฎ','ฑ','ธ','ํ','๊','ณ','ฯ','ญ',' ฐ',',','ฅ',
            'ฤ','ฆ','ฏ','โ','ฌ','็','๋','ษ','ศ','ซ','.',
            '(',')','ฉ','ฮ','ฺ','์','?','ฒ','ฬ','ฦ',' ']
            

dict_en = ['1','2','3','4','5','6','7','8','9','0','-','=',
            'q','w','e','r','t','y','u','i','o','p','[',']',"\\",
            'a','s','d','f','g','h','j','k','l',';',"\'",
            'z','x','c','v','b','n','m',',','.','/',
            '!','@','#','$','%','^','&','*','(',')','_','+',
            'Q','W','E','R','T','Y','U','I','O','P','{','}','|',
            'A','S','D','F','G','H','J','K','L',':','"',
            'Z','X','C','V','B','N','M','<','>','?',' ']



def entoth(text):
    text_list = []                                              # String
    index_output = []                                           # Interger
    printthis = ""

    text_list += text                                           # ยัดใน list ทีละตัว

    # ทำ loop หาตัวอักษรใน dict
    for o in range(len(text_list)):                               # loop หาใน dict_en ว่าเลขอะไร
        index_output = dict_en.index(text_list[o])

        printthis += dict_th[index_output]
    return printthis

def thtoen(text):
    text_list = []                                              # String
    index_output = []                                           # Interger
    printthis = ""

    text_list += text                                           # ยัดใน list ทีละตัว

    # ทำ loop หาตัวอักษรใน dict
    for o in range(len(text_list)):                               # loop หาใน dict_en ว่าเลขอะไร
        index_output = dict_th.index(text_list[o])

        printthis += dict_en[index_output]
    return printthis