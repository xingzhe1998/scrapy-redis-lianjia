import re
text = '''
        番禺-祈福新村-祈福新村C区
        /
        70㎡
        /南        /
          2室1厅1卫        
          /
          高楼层                        （3层）

'''


# print(re.sub(r'\s','',text))

lis = ['\n            ', '新上', '\n            ', '随时看房', '\n            ']
# lis_new = [re.sub('\s','',i) for i in lis]
# print([val.strip() for val in lis])
# ['', '新上', '', '随时看房', '']
# print([j for j in lis_new if j != ''])   # ''!=None
# print(''==None)
# print(type(''))