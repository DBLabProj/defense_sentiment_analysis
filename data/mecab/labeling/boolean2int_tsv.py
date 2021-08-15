
'''
디렉터리 내 모든 tsv 파일을
하나로 합치면서 True False를 1과 0으로 바꾸어줌

TSV 파일
[0] date [1] text [2] boolean
if True > 1
else > 0
'''
def rewrite(filename):
    with open(filename, "rt", encoding="utf-8") as f:
        lines = f.readlines()

    write_data = ""
    for l in lines:
        text, value = l.split("\t")[0], l.split("\t")[-1]
        
        if value.replace("\n", "") == "TRUE": i_val = "1"
        else: i_val = "0"
        write_data += text+"\t"+ i_val +"\n"

    return write_data

import glob
result = ""
for filename in glob.glob(".\\*.tsv"):
    result += rewrite(filename)

with open("dataset_2000.tsv", "wt", encoding="utf-8") as f:
    f.write(result)


