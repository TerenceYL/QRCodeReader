# 打包成一個執行檔
# pyinstaller --onefile --noconsole --add-binary "D:\Python\Python312\lib\site-packages\pyzbar;pyzbar" --add-binary "D:\Python\Python312\lib\site-packages\pylibdmtx;pylibdmtx" .\Output\BarcodeReader.py

import cv2
import qrcode
import pylibdmtx.pylibdmtx as dmtx  #3.12 才有裝此套件
from PIL import Image
import subprocess
from pyzbar.pyzbar import decode
import tkinter as tk
from tkinter import filedialog
import numpy as np
#from PIL import ImageGrab  #python 3.11 才可以用
import pyautogui    # require install pillow
import os
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename='BarcodeReader.log')

# 更新并计算 Canvas 的滚动区域
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))

# 創建一個函數來處理檔選擇操作
def select_file():
    file_path = filedialog.askopenfilename()  # 打開文件選擇對話方塊
    if file_path:
        process_image(file_path)

def select_file_datamatrix():
    file_path = filedialog.askopenfilename()  # 打開文件選擇對話方塊
    if file_path:
        process_image_datamatrix(file_path)

def select_file_datamatrix_iso88591():
    file_path = filedialog.askopenfilename()  # 打開文件選擇對話方塊
    if file_path:
        process_image_datamatrix_iso88591(file_path)

# 創建一個函數來處理圖像識別並更新文本標籤
def process_image(image_path):
    results_text.set("開始辨識..pyzbar")  # 清空文本標籤內容

    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    decoded_objects = decode(gray_image)
    
    qcd = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(image)

    objType = ""
    for obj in decoded_objects:
        objType = obj.type
        objData = obj.data
    if(objType == ''):
        # 可能辨識失敗，嘗試 一維碼
        # 在灰階圖像上解碼條碼
        decoded_objects = decode(gray_image)
        # 顯示檢測到的條碼資訊
        for obj in decoded_objects:
            objType = obj.type
            decode_result_text += obj.data
        decode_result_text = f'  條碼類型: {objType}\n┌────────　條碼內容　────────┐\n\n'
        
    else:
        decode_result_text = f'  條碼類型: {objType}\n┌────────　條碼內容　────────┐\n\n'
        for obj_cv2 in decoded_info:
            decode_result_text += f'{obj_cv2}\n'   

    decode_result_text += '\n\n└──────────────────────┘'

    result_text.insert(tk.END, decode_result_text + '\n')  # 更新文字方塊內容

    # cv2.imshow("Barcode Image", image)

    results_text.set("辨識結束")  # 清空文本標籤內容

def process_image_datamatrix(image_path):
    results_text.set("開始辨識..pyzbar")  # 清空文本標籤內容

    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用 DataMatrix 解碼庫尋找 DataMatrix
    datamatrix_objs = dmtx.decode(gray_image)

    decode_result_text = f'  條碼類型: Data Matrix\n┌────────　條碼內容　────────┐\n\n'

    # 在圖像中繪製 DataMatrix 的邊界框和解碼結果
    if datamatrix_objs:
        for obj in datamatrix_objs:
            try:
            # 解碼結果
                print("DataMatrix content:", obj.data.decode('utf-8'))
                decode_result_text += f'{obj.data.decode('utf-8')}\n'
            except Exception as e:
                logging.debug("Error: " + str(e))
                decode_result_text += str(e)

    decode_result_text += '\n\n└──────────────────────┘'

    result_text.insert(tk.END, decode_result_text + '\n')  # 更新文字方塊內容
    results_text.set("辨識結束")  # 清空文本標籤內容

def process_image_datamatrix_iso88591(image_path):
    results_text.set("開始辨識..pyzbar")  # 清空文本標籤內容

    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用 DataMatrix 解碼庫尋找 DataMatrix
    datamatrix_objs = dmtx.decode(gray_image)

    decode_result_text = f'  條碼類型: Data Matrix - ISO-8859-1\n┌────────　條碼內容　────────┐\n\n'

    # 在圖像中繪製 DataMatrix 的邊界框和解碼結果
    if datamatrix_objs:
        for obj in datamatrix_objs:
            try:
                # 解碼結果
                print("DataMatrix content:", obj.data.decode('iso-8859-1'))
                decode_result_text += f'{obj.data.decode('iso-8859-1')}\n'
            except Exception as e:
                logging.debug("Error: " + str(e))
                decode_result_text += str(e)

    decode_result_text += '\n\n└──────────────────────┘'

    result_text.insert(tk.END, decode_result_text + '\n')  # 更新文字方塊內容
    results_text.set("辨識結束")  # 清空文本標籤內容

# 創建一個函數來進行螢幕截圖、保存和識別
def screenshot_and_recognize():
    # 使用PyAutoGUI進行螢幕截圖
    #bbox = (1920, 0, 3840, 1080)  # 例如，這裡的座標表示捕獲第二個螢幕
    #screenshot = ImageGrab.grab(bbox)
    #screenshot = ImageGrab.grab()  #python 3.11 才可以用
    #screenshot = np.array(screenshot)

    screenshot = pyautogui.screenshot()
    
    # 保存截圖為影像檔
    screenshot_file = "screenshot.png"
    # cv2.imwrite(screenshot_file, cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)) # python 311

    # 保存截圖為影像檔 python 312 for pyautogui
    screenshot.save('screenshot.png')
    
    # 調用圖像識別函數處理截圖
    process_image(screenshot_file)

    # 删除文件
    if os.path.exists(screenshot_file):
        os.remove(screenshot_file)
        print(f"{screenshot_file} 已删除")
    else:
        print(f"{screenshot_file} 不存在")

def screenshot_and_recognize_datamatrix():
    # 使用PyAutoGUI進行螢幕截圖
    #bbox = (1920, 0, 3840, 1080)  # 例如，這裡的座標表示捕獲第二個螢幕
    #screenshot = ImageGrab.grab(bbox)
    #screenshot = ImageGrab.grab()  #python 3.11 才可以用
    #screenshot = np.array(screenshot)

    screenshot = pyautogui.screenshot()
    
    # 保存截圖為影像檔
    screenshot_file = "screenshot.png"
    # cv2.imwrite(screenshot_file, cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)) # python 311

    # 保存截圖為影像檔 python 312 for pyautogui
    screenshot.save('screenshot.png')
    
    # 調用圖像識別函數處理截圖
    process_image_datamatrix(screenshot_file)

    # 删除文件
    if os.path.exists(screenshot_file):
        os.remove(screenshot_file)
        print(f"{screenshot_file} 已删除")
    else:
        print(f"{screenshot_file} 不存在")

def screenshot_and_recognize_datamatrix_iso88591():
    # 進行螢幕截圖
    screenshot = pyautogui.screenshot()
    
    # 保存截圖為影像檔
    screenshot_file = "screenshot.png"
    # cv2.imwrite(screenshot_file, cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)) # python 311

    # 保存截圖為影像檔 python 312 for pyautogui
    screenshot.save('screenshot.png')
    
    # 調用圖像識別函數處理截圖
    process_image_datamatrix_iso88591(screenshot_file)

    # 删除文件
    if os.path.exists(screenshot_file):
        os.remove(screenshot_file)
        print(f"{screenshot_file} 已删除")
    else:
        print(f"{screenshot_file} 不存在")

def generate_qr_code(text, filename='qrcode.png'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)


def generate_data_matrix(text, filename='datamatrix.png'):
    # 將文字編碼為 DataMatrix 圖像
    dmx = dmtx.encode(text)

    # 將 DataMatrix 圖像轉換為 PIL 圖像
    pil_img = Image.frombytes('RGB', (dmx.width, dmx.height), dmx.pixels)
    pil_img.save(filename)

def text2qrcode():
    text = input_text.get("1.0", "end-1c")
    text_utf8 = text.encode('utf-8')
    filename = "Save_QRCode.png"
    generate_qr_code(text_utf8, filename)
    results_text.set(f"已生成 QR Code 並儲存為 {filename}")

    # 自動打開圖片
    try:
        #subprocess.Popen(['open', filename])  # 適用於 macOS
        subprocess.Popen(['start', '', filename], shell=True)  # 適用於 Windows
    except:
        pass

def text2datamatrix():
    text = input_text.get("1.0", "end-1c")
    text_utf8 = text.encode('utf-8')
    filename = "Save_DataMatrix.png"
    generate_data_matrix(text_utf8, filename)
    results_text.set(f"已生成 Data Matrix 並儲存為 {filename}")

    # 自動打開圖片
    try:
        #subprocess.Popen(['open', filename])  # 適用於 macOS
        subprocess.Popen(['start', '', filename], shell=True)  # 適用於 Windows
    except:
        pass

def text2datamatrix_iso88591():
    text = input_text.get("1.0", "end-1c")
    text_iso88591 = text.encode('iso-8859-1')
    filename = "Save_DataMatrix.png"
    generate_data_matrix(text_iso88591, filename)
    results_text.set(f"已生成 Data Matrix 並儲存為 {filename}")

    # 自動打開圖片
    try:
        #subprocess.Popen(['open', filename])  # 適用於 macOS
        subprocess.Popen(['start', '', filename], shell=True)  # 適用於 Windows
    except:
        pass

# 創建一個簡單的GUI視窗
    # v2.0: 辨識及產生 QR Code
    # v2.1: 增加辨識及產生 Data Matrix
root = tk.Tk()
root.title("條碼 Barcode / QR Code 辨識及轉換工具 (v2.1) Powered by TerenceYL ")
# 创建一个 Canvas
canvas = tk.Canvas(root)
canvas.pack(side='left', fill='both', expand=True)

# 创建一个滚动条
scrollbar = tk.Scrollbar(root, orient='vertical', command=canvas.yview)
scrollbar.pack(side='right', fill='y')

# 配置 Canvas 和滚动条
canvas.configure(yscrollcommand=scrollbar.set)

# 創建一個框架來包含按鈕和文字方塊，並使用grid佈局
frame = tk.Frame(canvas)
#frame.grid(row=1, column=1)
canvas.create_window((0, 0), window=frame, anchor='nw')
frame.bind('<Configure>', on_configure)


# 創建一個按鈕用於選擇檔，並將其置於框架的左側
select_button = tk.Button(frame, text="選擇圖檔來辨識 QR Code", command=select_file)
select_button.grid(row=1, column=1, padx=10, pady=5)

select_datamatrix_button = tk.Button(frame, text="選擇圖檔來辨識 Data Matrix - utf-8", command=select_file_datamatrix)
select_datamatrix_button.grid(row=2, column=1, padx=10, pady=5)

select_datamatrix_iso88591_button = tk.Button(frame, text="選擇圖檔來辨識 Data Matrix - ISO-8859-1", command=select_file_datamatrix_iso88591)
select_datamatrix_iso88591_button.grid(row=3, column=1, padx=10, pady=5)

# 創建一個按鈕用於進行螢幕截圖並識別
screenshot_button = tk.Button(frame, text="螢幕截圖並辨識 QR Code", command=screenshot_and_recognize)
screenshot_button.grid(row=1, column=2, padx=20, pady=5)

screenshot_datamatrix_button = tk.Button(frame, text="螢幕截圖並辨識 Data Matrix - utf-8", command=screenshot_and_recognize_datamatrix)
screenshot_datamatrix_button.grid(row=2, column=2, padx=20, pady=5)

screenshot_datamatrix_ISO88591_button = tk.Button(frame, text="螢幕截圖並辨識 Data Matrix - ISO-8859-1", command=screenshot_and_recognize_datamatrix_iso88591)
screenshot_datamatrix_ISO88591_button.grid(row=3, column=2, padx=20, pady=5)

# 創建一個按鈕，用來把文字轉成 QR Code
trans2qrcode_button = tk.Button(frame, text="文字轉QR Code - utf-8", command=text2qrcode)
trans2qrcode_button.grid(row=1, column=3, padx=20, pady=5)

# 創建一個按鈕，用來把文字轉成 Data Matrix
trans2datamatrix_button = tk.Button(frame, text="文字轉Data Matrix - utf-8", command=text2datamatrix)
trans2datamatrix_button.grid(row=2, column=3, padx=20, pady=5)

# 創建一個按鈕，用來把文字轉成 Data Matrix - ISO-8859-1
trans2datamatrix_ISO88591_button = tk.Button(frame, text="文字轉Data Matrix - ISO-8859-1", command=text2datamatrix_iso88591)
trans2datamatrix_ISO88591_button.grid(row=3, column=3, padx=20, pady=5)

canvas.config(scrollregion=canvas.bbox('all'))
print('top-width',frame.winfo_width(), 'top-height', frame.winfo_height())
frame.update_idletasks()
print('top-width',frame.winfo_width(), 'top-height', frame.winfo_height())

frame2 = tk.Frame(canvas)
#frame2.grid(row=2, column=1)
canvas.create_window((0, frame.winfo_height() +10), window=frame2, anchor='nw')
frame2.bind('<Configure>', on_configure)
print('down-width',frame2.winfo_width(), 'down-height', frame2.winfo_height())

# 創建一個文本標籤用於顯示識別結果
results_text = tk.StringVar()
result_label = tk.Label(frame2, textvariable=results_text)
result_label.grid(row=1, column=1, padx=20, pady=0)

# 創建一個文本標籤用於說明文字方塊的功能
scr_recog_label = tk.Label(frame2, text="辨識出來的文字結果")
scr_recog_label.grid(row=1, column=1, padx=20, pady=0, sticky=tk.W)

# 創建一個文字方塊用於顯示識別結果
result_text = tk.Text(frame2, wrap=tk.WORD, height=20, width=100)
result_text.grid(row=2, column=1, padx=10, pady=10)

# 創建一個文本標籤用於說明文字方塊的功能
transqrcode_label = tk.Label(frame2, text="輸入轉換成QR Code 的文字")
transqrcode_label.grid(row=3, column=1, padx=20, pady=0, sticky=tk.W)

# 創建一個文字方塊用於輸入要轉成 QR Code / Data Matrix 的文字
input_text = tk.Text(frame2, wrap=tk.WORD, height=10, width=100)
input_text.grid(row=4,column=1, padx=10, pady=10)


# 計算視窗的大小以適應所有元件
print('top-width',frame.winfo_width(), 'down',frame2.winfo_width())
print('top-height',frame.winfo_height(), 'down',frame2.winfo_height())
canvas.config(scrollregion=canvas.bbox('all'))
root.update_idletasks()
frame.update_idletasks()
frame2.update_idletasks()
print('top-width',frame.winfo_width(), 'down',frame2.winfo_width())
print('top-height',frame.winfo_height(), 'down',frame2.winfo_height())
window_width = max(frame.winfo_width(), frame2.winfo_width()) + 50  # 加上一些额外空间
window_height = frame.winfo_height() + frame2.winfo_height() + 50  # 加上一些额外空间

# 設置視窗大小
root.geometry(f"{window_width}x{window_height}")


try:
    # 啟動GUI主迴圈
    root.mainloop()
except KeyboardInterrupt:
    print("再見！")