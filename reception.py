import tkinter as tk
from tkinter import ttk, messagebox
from itemBase import itemBase

class ItemManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("物品复活软件 - 大学生物品交换平台")
        self.root.geometry("800x600")
        
        self.itemBase = itemBase()
        
        # 创建主框架
        mainFrame = ttk.Frame(root, padding="10")
        mainFrame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainFrame.columnconfigure(1, weight=1)
        mainFrame.rowconfigure(4, weight=1)
        
        # 标题
        titleLabel = ttk.Label(mainFrame, text="物品复活软件", font=("Arial", 16, "bold"))
        titleLabel.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 功能按钮框架
        buttonFrame = ttk.Frame(mainFrame)
        buttonFrame.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # 按钮
        ttk.Button(buttonFrame, text="添加物品", command=self.addItem).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttonFrame, text="搜索物品", command=self.searchItem).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttonFrame, text="删除物品", command=self.deleteItem).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttonFrame, text="显示所有物品", command=self.showAllItems).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttonFrame, text="退出程序", command=self.exitProgram).pack(side=tk.LEFT, padx=5)
        
        # 搜索框
        searchFrame = ttk.Frame(mainFrame)
        searchFrame.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        ttk.Label(searchFrame, text="搜索关键词:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(searchFrame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<Return>', lambda event: self.search_item())
        
        # 结果显示区域
        resultFrame = ttk.Frame(mainFrame)
        resultFrame.grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S))
        resultFrame.columnconfigure(0, weight=1)
        resultFrame.rowconfigure(0, weight=1)
        
        # 创建树形视图显示物品
        columns = ('ID', '名称', '价格', '描述', '所有者', '联系方式')
        self.tree = ttk.Treeview(resultFrame, columns=columns, show='headings', height=15)
        
        # 定义列
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(resultFrame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 状态栏
        self.statusVar = tk.StringVar()
        self.statusVar.set(f"当前共有 {self.itemBase.itemNum} 件物品")
        statusBar = ttk.Label(mainFrame, textvariable=self.statusVar, relief=tk.SUNKEN)
        statusBar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # 初始显示所有物品
        self.refresh_item_list()

    def addItem(self):
        # 创建添加物品对话框
        dialog = AddItemDialog(self.root)
        self.root.wait_window(dialog.top)
        
        if dialog.result:
            name, price, description, owner, contact = dialog.result
            result = self.itemBase.addItem(name, price, description, owner, contact)
            messagebox.showinfo("添加结果", result)
            self.refresh_item_list()

    def searchItem(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showwarning("输入错误", "请输入搜索关键词")
            return
        
        results = self.itemBase.searchItem(keyword)
        self.update_treeview(results)
        self.status_var.set(f"搜索到 {len(results)} 件匹配物品")

    def deleteItem(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("选择错误", "请先选择要删除的物品")
            return
        
        item_id = int(self.tree.item(selected[0])['values'][0])
        item_name = self.tree.item(selected[0])['values'][1]
        
        if messagebox.askyesno("确认删除", f"确定要删除物品 '{item_name}' 吗？"):
            result = self.itemBase.deleteItem(item_id)
            messagebox.showinfo("删除结果", result)
            self.refresh_item_list()

    def showAllItems(self):
        self.refresh_item_list()
        self.status_var.set(f"显示所有 {self.itemBase.itemNum} 件物品")

    def refresh_item_list(self):
        all_items = self.itemBase.showAllItems()
        self.update_treeview(all_items)
        self.statusVar.set(f"当前共有 {self.itemBase.itemNum} 件物品")

    def update_treeview(self, items_df):
        # 清空树形视图
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加新数据
        if not items_df.empty:
            for idx, row in items_df.iterrows():
                self.tree.insert('', tk.END, values=(
                    idx, 
                    row['Name'], 
                    row['Price'], 
                    row['Description'][:50] + "..." if len(str(row['Description'])) > 50 else row['Description'],
                    row['Owner'],
                    row['Contact']
                ))

    def exitProgram(self):
        if messagebox.askyesno("退出确认", "确定要退出程序吗？"):
            self.itemBase.closeAndSave()
            self.root.destroy()


class AddItemDialog:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("添加新物品")
        self.top.geometry("400x300")
        self.top.transient(parent)
        self.top.grab_set()
        
        self.result = None
        
        # 创建表单
        frame = ttk.Frame(self.top, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 物品名称
        ttk.Label(frame, text="物品名称:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 物品价格
        ttk.Label(frame, text="物品价格:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.price_entry = ttk.Entry(frame, width=30)
        self.price_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 物品描述
        ttk.Label(frame, text="物品描述:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.desc_text = tk.Text(frame, width=30, height=5)
        self.desc_text.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 所有者
        ttk.Label(frame, text="所有者:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.owner_entry = ttk.Entry(frame, width=30)
        self.owner_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 联系方式
        ttk.Label(frame, text="联系方式:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.contact_entry = ttk.Entry(frame, width=30)
        self.contact_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="添加", command=self.ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.cancel).pack(side=tk.LEFT, padx=5)
        
        # 配置网格权重
        frame.columnconfigure(1, weight=1)
        self.top.columnconfigure(0, weight=1)
        
        # 设置焦点
        self.name_entry.focus()

    def ok(self):
        name = self.name_entry.get().strip()
        price = self.price_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        owner = self.owner_entry.get().strip()
        contact = self.contact_entry.get().strip()
        
        if not name:
            messagebox.showwarning("输入错误", "物品名称不能为空")
            return
        
        self.result = (name, price, description, owner, contact)
        self.top.destroy()

    def cancel(self):
        self.top.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ItemManagerGUI(root)
    root.mainloop()