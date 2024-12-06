import unittest


def fullwidth_to_halfwidth(s):
    """
    将文本中的全角字符转换为半角字符
    """
    s = s.replace("【", "[").replace("】", "]")
    halfwidth_str = ""
    for char in s:
        code = ord(char)
        if code == 12288:  # 全角空格直接转换
            code = 32
        elif code == 65509: # ￥ ¥
            code = 165
        elif code == 65111: # ﹗ !
            code = 33
        elif code == 65105: # ﹑、
            code = 12289
        elif code == 65117: # ﹝ 〔
            code = 12308
        elif code == 65118:
            code = 12309  # ﹞ 〕
        elif 65281 <= code <= 65374:  # 全角字符（除空格）根据关系转化
            code -= 65248
        halfwidth_str += chr(code)
    return halfwidth_str


# def special_token(s):
#     s = s.replace("【", "[").replace("】", "]")
#     s = s.replace("（", "(").replace("）", ")")
#     s = s.replace("《", "<").replace("》", ">")
#     s = s.replace("‘", "'").replace("’", "'")
#     s = s.replace("“", '"').replace("”", '"')
#     s = s.replace("：", ":")
#     s = s.replace("。", ".")
#     s = s.replace("；", ";")
#     s = s.replace("！", "!")
#     s = s.replace("～", "~")
#     s = s.replace("，", ",")
#     s = s.replace("—", "-")
#     s = s.replace("？", "?")
#     return s


class TestConvertToHalfwidth(unittest.TestCase):
    def test_convert_to_halfwidth(self):
        # 测试转换结果是否正确
        self.assertEqual(fullwidth_to_halfwidth("ＡＢＣｄｅｆ"), "ABCdef")
        self.assertEqual(fullwidth_to_halfwidth("１２３４５６７８９０"), "1234567890")
        self.assertEqual(fullwidth_to_halfwidth("Ｈｅｌｌｏ，Ｗｏｒｌｄ！"), "Hello,World!")
        self.assertEqual(fullwidth_to_halfwidth("ａｂｃＤＥＦＧＨｉＪＫｌｍＮｏＰｑＲＳＴｕＶＷＸｙＺ"),
                         "abcDEFGHiJKlmNoPqRSTuVWXyZ")
        self.assertEqual(fullwidth_to_halfwidth("ＡＢＣｄｅｆ１２３４５６７８９０！＠＃＄％＾＆＊（）—＋＝｜｛｝【】；：＇＂＜＞，．？／"),
                         "ABCdef1234567890!@#$%^&*()—+=|{}[];:'\"<>,.?/")
        
if __name__ == '__main__':
    # unittest.main()

    str_u = "﹑﹗﹝﹞﹢！＂＃＄％＆＇（）＊＋，－．／０１２３４５６７８９：；＜＝＞？ＡＢＣＤＥＦＧＨＩＫＬＭＮＯＰＲＳＴＵＶＷＹＺ［］｀ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｒｓｔｕｚ｛｜｝～￠￡￥𣇉"
    ref_str_u = fullwidth_to_halfwidth(str_u)
    print(str_u)
    print(ref_str_u)