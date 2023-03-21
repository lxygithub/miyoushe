import tkinter as tk
from tkinter import filedialog


class App:

    # create the GUI main window

    def __init__(self):
        super().__init__()
        self.text_output = None
        self.checkbox = None
        self.lbl_log = None
        self.start = None
        self.folder_path = ""
        self.lbl_path = None

        self.__text_post_id = None

    def create_window(self):
        win = tk.Tk()
        win.title("米游社图片下载器")
        win.minsize(600, 400)

        # create the GUI widgets
        frame1 = tk.Frame(win)
        lbl_post_id = tk.Label(frame1, text="输入post_id")
        self.__text_post_id = tk.Entry(frame1)
        lbl_post_id.pack(side="left")
        self.__text_post_id.pack(side="left")

        frame2 = tk.Frame(win)
        btn_start = tk.Button(frame2, text="开始下载", command=self.start)
        btn_select = tk.Button(frame2, text="选择保存目录", command=self.__select_folder)
        self.lbl_path = tk.Label(frame2, text=":")
        btn_start.pack(side="left")
        btn_select.pack(side="left", padx=10)
        self.lbl_path.pack(side="left")

        self.lbl_log = tk.Label(win, text="日志:")
        self.text_output = tk.Text(win, state="disabled")

        # pack the widgets into the window grid
        frame1.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nw", padx=10, pady=10)

        frame2.grid(row=1, column=0, sticky="nw", padx=10)

        self.lbl_log.grid(row=3, column=0, sticky="nw", padx=10)
        self.text_output.grid(row=4, column=0, columnspan=6, padx=(10, 10), pady=(0, 10))

        self.checkbox = tk.Checkbutton(win, text="是否废图开启筛选模式")
        self.checkbox.grid(row=5, column=0, sticky="nw", padx=10)

        # start the main event loop
        win.mainloop()

    # define the event functions
    def __select_folder(self):
        self.folder_path = filedialog.askdirectory()
        self.__display_folder()

    def __display_folder(self):
        self.lbl_path.config(text=f"{self.folder_path}")
        self.lbl_path.update()

    def get_post_id(self):
        return self.__text_post_id.get()

    def get_filter_checked(self):
        return self.checkbox.get()

    def output_log(self, log):
        self.text_output.configure(state="normal")
        self.text_output.insert(tk.END, f"\n{log}")
        self.text_output.configure(state="disabled")
