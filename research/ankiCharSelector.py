charsNotUsedIn10kWords = ["腹", "丑", "霸", "霍", "仇", "抚", "赫", "翰", "舱", "玛", "涌", "郁", "宏", "桑", "丹",
                          "鹏", "玄", "俩", "侯", "凯", "辖", "迪", "纹", "艾", "抖", "皱", "卧", "胎", "卢", "贺",
                          "颤", "悬", "津", "魔", "妖", "莉", "桂", "役", "逆", "牧", "愚", "祥", "昏", "韦", "瑟",
                          "掠", "匆", "昨", "邪", "竭", "柳", "尘", "葛", "贤", "戈", "乔", "歼", "浩", "拳", "姆",
                          "舰", "履", "函", "兹", "扔", "歇", "袁", "冬", "乳", "奸", "弗", "缝", "侍", "仆", "魏",
                          "炮", "毅", "汪", "凤", "拦", "兽", "凌", "晨", "唐", "豆", "讼", "茨", "浑", "玲", "卜",
                          "珠", "押", "扁", "秋", "磁", "晴", "昌", "蒂", "横", "蓄", "棉", "御", "吕", "陵", "粉",
                          "柴", "鲁", "沃", "冯", "薛", "铃", "吞", "窝", "梁", "柯", "穆", "凶", "芳", "娜", "膜",
                          "侠", "滚", "蜂", "侧", "剂", "俊", "曼", "晃", "逊", "闲", "艇", "芬", "吉", "鸿", "狠",
                          "吻", "邓", "溜", "劫", "爵", "柱", "苍", "岳"]

phoneticCharsOutsideTop2k = ["彔", "來", "於", "亻", "冋", "匽", "乂", "㝵", "臽", "長", "菐", "夆", "叉", "丙", "畏",
                             "羅", "昜", "呙", "囗", "時", "氐", "贞", "侖", "蒦", "敖", "㐬", "冓", "厓", "賴", "艮",
                             "肖", "齊", "甬", "尉", "仑", "禾", "烏", "奚", "畐", "婁", "堇", "無", "丨", "夕", "夅",
                             "旱", "間", "幾", "艹", "辰", "聶", "詹", "甫", "巠", "庸", "岡", "娄", "丩", "麗", "戉",
                             "屯", "鹿", "矞", "睪", "亥", "執", "丶", "悤", "禽", "韋", "爭", "戔", "牟", "犮", "㝉",
                             "匋", "劦", "乞", "冈", "卑", "叟", "華", "闌", "聂", "冥", "邑", "責", "勞", "孚", "嬰",
                             "辟", "乍", "夌", "匕", "崩", "阑", "匡", "脊", "遂", "婴", "卯", "罔", "厥", "冂", "㐱",
                             "酉", "巳", "彡", "臿", "雚", "宛", "耒", "啇", "卂", "風", "旬", "襄", "區", "畢", "貞",
                             "奂", "虍", "圭", "熏", "豈", "會", "龍", "龠", "囊", "斿", "厲", "連", "勹", "門", "咢",
                             "將", "鬲", "豊", "奐", "寧", "見", "奄", "眇", "爿", "疌", "尃", "賏", "尋", "亢", "佘",
                             "彐", "當", "喬", "咼", "倉", "農", "厄", "歷", "雍", "覽", "亞", "壯", "丸", "賓", "夾",
                             "盡", "壬", "單", "馬", "臼", "刃", "臾", "隹", "戋", "愛", "夷", "貝", "敫", "敝", "卞",
                             "盧", "俞", "亭", "辡"]

searchString = ""
for hanzi in charsNotUsedIn10kWords:
    searchString += f"hanzi:{hanzi} OR "

print(searchString)