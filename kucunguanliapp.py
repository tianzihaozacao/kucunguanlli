import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Product:
    def __init__(self, name, color, category, size, quantity):
        self.name = name
        self.color = color
        self.category = category
        self.size = size
        self.quantity = quantity


class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)
        self.products.sort(key=lambda x: (x.category, x.name))  # 按分类和名称对产品进行排序

    def get_inventory_details(self):
        return [(product.name, product.color, product.category, product.size, product.quantity) for product in
                self.products]

    def update_quantity(self, product_name, new_quantity):
        for product in self.products:
            if product.name == product_name:
                product.quantity = new_quantity
                break

    def update_listbox(self, listbox):
        listbox.delete(0, tk.END)
        inventory_details = self.get_inventory_details()
        for item in inventory_details:
            listbox.insert(tk.END,
                           f"名称: {item[0]}, 颜色: {item[1]}, 分类: {item[2]}, 尺码: {item[3]}, 数量: {item[4]}")


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("库存管理")

        self.inventory = Inventory()

        self.label = tk.Label(root, text="库存管理", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(root, width=50, height=10, selectmode="BROWSE", activestyle='none')
        self.listbox.pack(pady=10)
        self.listbox.bind("<Double-1>", self.edit_quantity)  # 双击触发编辑数量

        self.add_button = tk.Button(root, text="添加产品", command=self.add_product)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.delete_button = tk.Button(root, text="删除产品", command=self.delete_product)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.display_button = tk.Button(root, text="显示库存", command=self.display_inventory)
        self.display_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.update_button = tk.Button(root, text="编辑数量", command=self.update_quantity_from_listbox)
        self.update_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # 添加排序按钮
        self.sort_quantity_button = tk.Button(root, text="升序", command=lambda: self.sort_listbox("升序"))
        self.sort_quantity_button.pack(side=tk.TOP, padx=10, pady=10)
        self.sort_quantity_button = tk.Button(root, text="降序", command=lambda: self.sort_listbox("降序"))
        self.sort_quantity_button.pack(side=tk.TOP, padx=10, pady=10)

        self.update_listbox()

    def add_product(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("添加产品")

        name_label = tk.Label(add_window, text="名称:")
        name_label.grid(row=0, column=0, pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, pady=5)

        color_label = tk.Label(add_window, text="颜色:")
        color_label.grid(row=1, column=0, pady=5)
        color_entry = tk.Entry(add_window)
        color_entry.grid(row=1, column=1, pady=5)

        category_label = tk.Label(add_window, text="分类:")
        category_label.grid(row=2, column=0, pady=5)
        category_combobox = ttk.Combobox(add_window, values=["童装", "服装"])
        category_combobox.grid(row=2, column=1, pady=5)

        size_label = tk.Label(add_window, text="尺码:")
        size_label.grid(row=3, column=0, pady=5)
        size_combobox = ttk.Combobox(add_window)
        size_combobox.grid(row=3, column=1, pady=5)

        quantity_label = tk.Label(add_window, text="数量:")
        quantity_label.grid(row=4, column=0, pady=5)
        quantity_spinbox = tk.Spinbox(add_window, from_=0, to=1000)  # 设置数量范围
        quantity_spinbox.grid(row=4, column=1, pady=5)

        category_combobox.bind("<<ComboboxSelected>>",
                               lambda event: self.update_size_combobox(size_combobox, category_combobox.get()))
        category_combobox.set("童装")  # 默认选择童装
        self.update_size_combobox(size_combobox, "童装")

        submit_button = tk.Button(add_window, text="提交",
                                  command=lambda: self.submit_product(name_entry.get(), color_entry.get(),
                                                                      category_combobox.get(), size_combobox.get(),
                                                                      quantity_spinbox.get(), add_window))
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def submit_product(self, name, color, category, size, quantity, add_window):
        try:
            quantity = int(quantity)
            if quantity < 0:
                raise ValueError("数量必须是非负整数.")

            product = Product(name, color, category, size, quantity)
            self.inventory.add_product(product)
            messagebox.showinfo("成功", "产品已添加到库存.")
            add_window.destroy()
            self.update_listbox()

        except ValueError as e:
            messagebox.showerror("错误", str(e))

    def delete_product(self):
        selected_product_name = self.listbox.get(tk.ACTIVE)
        if not selected_product_name:
            messagebox.showwarning("警告", "请选择要删除的产品.")
            return

        confirm = messagebox.askyesno("确认删除", f"是否确认删除产品: {selected_product_name}？")
        if confirm:
            self.inventory.remove_product(selected_product_name.split(":")[1].strip())
            self.update_listbox()

    def update_listbox(self):
        self.inventory.update_listbox(self.listbox)

    def display_inventory(self):
        display_window = tk.Toplevel(self.root)
        display_window.title("库存显示")

        selected_product = tk.StringVar()
        selected_product.set(self.listbox.get(tk.ACTIVE))

        product_label = tk.Label(display_window, text="选择产品:")
        product_label.pack(pady=5)

        product_listbox = tk.Listbox(display_window, width=50, height=10)
        product_listbox.pack(pady=10)
        product_listbox.bind("<Double-1>", lambda event: self.edit_quantity(event, selected_product.get()))

        update_button = tk.Button(display_window, text="更新数量",
                                  command=lambda: self.update_quantity(selected_product.get(),
                                                                       new_quantity_entry.get()))
        update_button.pack(pady=5)

        new_quantity_label = tk.Label(display_window, text="新数量:")
        new_quantity_label.pack(pady=5)
        new_quantity_entry = tk.Entry(display_window)
        new_quantity_entry.pack(pady=5)

        product_listbox.bind("<ButtonRelease-1>", lambda event: selected_product.set(product_listbox.get(tk.ACTIVE)))
        product_listbox.insert(tk.END, *[" ".join(map(str, item)) for item in self.inventory.get_inventory_details()])

    def edit_quantity(self, event, selected_product_name):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("编辑数量")

        selected_product = None
        for product in self.inventory.products:
            if product.name == selected_product_name:
                selected_product = product
                break

        if selected_product is not None:
            quantity_label = tk.Label(edit_window, text=f"{selected_product.name} 的数量:")
            quantity_label.pack(pady=5)

            quantity_entry = tk.Entry(edit_window)
            quantity_entry.insert(0, selected_product.quantity)
            quantity_entry.pack(pady=5)

            update_button = tk.Button(edit_window, text="更新数量",
                                      command=lambda: self.update_quantity(selected_product.name, quantity_entry.get(),
                                                                           edit_window))
            update_button.pack(pady=5)

    def update_quantity_from_listbox(self):
        selected_product_name = self.listbox.get(tk.ACTIVE)
        edit_window = tk.Toplevel(self.root)
        edit_window.title("编辑数量")

        selected_product = None
        for product in self.inventory.products:
            if product.name in selected_product_name:
                selected_product = product
                break

        if selected_product is not None:
            quantity_label = tk.Label(edit_window, text=f"{selected_product.name} 的数量:")
            quantity_label.pack(pady=5)

            quantity_entry = tk.Entry(edit_window)
            quantity_entry.insert(0, selected_product.quantity)
            quantity_entry.pack(pady=5)

            update_button = tk.Button(edit_window, text="更新数量",
                                      command=lambda: self.update_quantity(selected_product.name, quantity_entry.get(),
                                                                           edit_window))
            update_button.pack(pady=5)

    def update_quantity(self, product_name, new_quantity, edit_window):
        try:
            new_quantity = int(new_quantity)
            if new_quantity < 0:
                raise ValueError("新数量必须是非负整数.")

            self.inventory.update_quantity(product_name, new_quantity)
            messagebox.showinfo("成功", "数量已更新.")
            self.update_listbox()
            edit_window.destroy()  # 关闭编辑窗口

        except ValueError as e:
            messagebox.showerror("错误", str(e))

    def update_size_combobox(self, size_combobox, category):
        if category == "童装":
            sizes = ["70", "80", "90", "100", "110", "120", "130", "140", "150", "160", "170"]
        elif category == "服装":
            sizes = ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL"]
        else:
            sizes = []
        size_combobox['values'] = sizes
        size_combobox.set(sizes[0])  # 设置默认选择第一个尺码

    def sort_listbox(self, order):
        if order == "升序":
            self.inventory.products.sort(key=lambda x: x.quantity)
        elif order == "降序":
            self.inventory.products.sort(key=lambda x: x.quantity, reverse=True)
        self.update_listbox()


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
