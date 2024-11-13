#-*- coding : utf-8-*-
import tkinter
from tkinterdnd2 import DND_FILES, TkinterDnD, tkdnd
from tkinter import messagebox
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import switchbu5g
import threading  # 导入 threading 模块
import sys
# 定义拖放事件处理函数

def drop(event):
    file_path = event.data.strip()
    file_path = file_path.strip("{}")  # 处理 Windows 路径
    entry_sv.set(file_path)
    print(f"拖入的文件路径: {file_path}")

def drop1(event):
    file_path1 = event.data.strip()
    file_path1 = file_path1.strip("{}")  # 处理 Windows 路径
    entry_sv1.set(file_path1)
    print(f"拖入的文件路径: {file_path1}")    

def drop2(event):
    file_path2 = event.data.strip()
    file_path2 = file_path2.strip("{}")  # 处理 Windows 路径
    entry_sv2.set(file_path2)
    print(f"拖入的文件路径: {file_path2}")

def drop3(event):
    file_path3 = event.data.strip()
    file_path3 = file_path3.strip("{}")  # 处理 Windows 路径
    entry_sv3.set(file_path3)
    print(f"拖入的文件路径: {file_path3}")

def process_file():
    file_path1 = entry_sv.get().strip()  # 获取文件路径
    file_path2 = entry_sv1.get().strip() 
    file_path3 = entry_sv2.get().strip()
    file_path4 = entry_sv3.get().strip()
    if not file_path1:
        print("没有拖放文件！")
        return
    df = pd.read_csv(file_path1, encoding='gbk')
    # 确保在这里 index 参数使用列表形式
    plv = pd.pivot_table(df, index=['CGI'], values=['是否高负荷'], aggfunc='sum')
    plv = plv.loc[plv['是否高负荷'] == 1]

    nrcell = pd.read_excel(file_path2, sheet_name='NRCell', engine='openpyxl')
    sectorf = pd.read_excel(file_path2, sheet_name='SectorFunction', engine='openpyxl')
    bu = pd.read_excel(file_path2, sheet_name='BBU', engine='openpyxl')
    cell4gtdd=pd.read_excel(file_path4, sheet_name='Cell4GTDD', engine='openpyxl')

    # 建立输出文件
    newdf=pd.DataFrame()
    newdf.to_excel(file_path3, sheet_name='Sheet1', index=False)
    data1 = {'CGI':[],'方案':[]}

    # 遍历plv
    for i in plv.index:
        i3, i4, i1, i2 = i.split('-', 3)
        print(f"CGI:{i}")
        n = 1
        m = 1
        x = 0
        y = 0
        bf_list = [0]*30
        sf_list = [0]*30
        # 统计基带资源种类与数量
        filtered_nracell = nrcell[nrcell['ManagedElement'] == i1]
        vc = filtered_nracell['refBpPoolFunction'].value_counts()
        vc = vc.to_dict()
        # 根据CGI获取小区数据
        for index, row in nrcell.iterrows():
            if row['ManagedElement'] == i1:
                cell = row['cellLocalId']
                sf = row['refSectorFunction']
                bf = row['refBpPoolFunction']
                band = row['CarrierDL_nrbandwidth']
                freq = row['CarrierUL_frequency']
                mark = 0
                print(f"扇区={sf}, 基带={bf}, 带宽={band}, 频率={freq}")
                # 将基带与扇区资源写入列表
                bf_list[n] = bf
                sf_list[m] = sf
                n += 1
                m += 1
                for index_S, row_S in sectorf.iterrows():
                    if row_S['moId'] == sf and row_S['ManagedElement'] == i1:
                        ru = row_S['RUId']
                        tr = row_S['RxChannelNo']
                        tr = tr[2:4]
                        sfP = row_S['sectorFreqPower']
                        print(f"ru={ru}, 通道={tr}, 频段与功率={sfP}")

                for index_B, row_B in bu.iterrows():
                    if row_B['bpPoolFunction'] == bf and row_B['ManagedElement'] == i1:
                        buname = row_B['name']
                        print(f"buname={buname}")
                # 匹配高负荷小区相关参数            
                if i2 == cell:
                    print(f"*高负荷小区匹配成功*")
                    mark = 0
                    keysf = sf
                    keybf = bf
                    keytr = tr
                    keybu = '' + buname + ''
                print(' ')
        for index, row_x in cell4gtdd.iterrows():
            if row_x['ManagedElement'] == i1 and row_x['sectorFunctionId'] == keysf:
                mark2 = 1
            else:
                mark2 = 0
        # 判断超级小区
        test = ";"
        if keysf.find(test) != -1:
            data1['CGI'].append(i)
            data1['方案'].append(f"超级小区拆分")
            print(f"超级小区拆分")
        else:
            # 判断基带数量
            for count in bf_list:
                if count == keybf:
                    x += 1
            # 判断扇区数量
            keycount = switchbu5g.switchbu(str(keybu), int(keytr))
            print(switchbu5g.switchbu(str(keybu), int(keytr)))
            for countsf in sf_list:
                if countsf == keysf:
                    mark += 1
            print(keybu, keytr, keybf, x, mark)
            if mark == 2:
                data1['CGI'].append(i)
                data1['方案'].append(f"已扩容,不做处理")
                print(f"已扩容,不做处理")        
            elif mark!= 2 and x < keycount and x!= 0 and mark2 != 1:
                data1['CGI'].append(i)
                data1['方案'].append(f"{x + 1}槽软扩后60m")
                print(f"{x + 1}槽软扩后60m")
            elif x < keycount and x == 0:
                data1['CGI'].append(i)
                data1['方案'].append(f"非2.6g小区,不做处理")
            elif mark2 == 1:
                data1['CGI'].append(i)
                data1['方案'].append(f"已做4g扩容,不做处理")
            elif x == keycount and keytr == 2:
                judgelist = []
                for index_C, row_C in bu.iterrows():
                    for key2, value2 in vc.items():
                        if row_C['bpPoolFunction'] == key2 and row_C['ManagedElement'] == i1:
                            judgebu=''+row_C['name']+''
                            judge = switchbu5g.switchbu(str(judgebu), 2)
                            if judge != 0 and value2 < judge:
                                judgelist.append(key2)
                if judgelist is not None:
                    data1['CGI'].append(i)
                    data1['方案'].append(f"{judgelist}可扩容")
                    print(f"{judgelist}可扩容")
                else:
                    data1['CGI'].append(i)
                    data1['方案'].append(f"新增基带板{keybu}")
                    print(f"新增基带板{keybu}")
            elif x == keycount and keytr != 2:
                data1['CGI'].append(i)
                data1['方案'].append(f"新增基带板{keybu}并跳纤至新增基带板扩容")
                print(f"新增基带板{keybu}并跳纤至新增基带板扩容")
    sheet=pd.DataFrame(data1)
    sheet.to_excel(file_path3, sheet_name='Sheet1', index=False, startrow=1)
    messagebox.showinfo("处理完成", "文件处理完成！")

def start_processing():
    # 在按钮被按下时启动一个新线程来处理文件
    threading.Thread(target=process_file).start()

# 主程序界面
root = TkinterDnD.Tk()
root.title("5g容量处理")
root.geometry("700x360")

label = tkinter.Label(root, text="请将负荷表csv拖入此处1")
label.pack()

entry_sv = tkinter.StringVar()
entry = tkinter.Entry(root, textvariable=entry_sv, width=80)
entry.pack()

label1 = tkinter.Label(root, text="请将5g小区表xlsm拖入此处2")
label1.pack()

entry_sv1 = tkinter.StringVar()
entry1 = tkinter.Entry(root, textvariable=entry_sv1, width=80)
entry1.pack()

label3 = tkinter.Label(root, text="请将(4g)对照表xlsm拖入此处3")
label3.pack()

entry_sv3 = tkinter.StringVar()
entry3 = tkinter.Entry(root, textvariable=entry_sv3, width=80)
entry3.pack()

label2 = tkinter.Label(root, text="输出文件xlsm")
label2.pack()

entry_sv2 = tkinter.StringVar()
entry2 = tkinter.Entry(root, textvariable=entry_sv2, width=80)
entry2.pack()

entry.drop_target_register(DND_FILES)
entry.dnd_bind('<<Drop>>', drop)

entry1.drop_target_register(DND_FILES)
entry1.dnd_bind('<<Drop>>', drop1)

entry2.drop_target_register(DND_FILES)
entry2.dnd_bind('<<Drop>>', drop2)

entry3.drop_target_register(DND_FILES)
entry3.dnd_bind('<<Drop>>', drop3)

button = tkinter.Button(root, text="开始处理", command=start_processing)
button.pack(pady=20, anchor="center")

root.mainloop()
