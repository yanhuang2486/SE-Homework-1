import pandas as pd
import os

class itemBase():

    def __init__(self):
        # 如果文件不存在，创建一个空的DataFrame
        if os.path.exists('itemBase.xlsx'):
            self.items = pd.read_excel('itemBase.xlsx')
        else:
            self.items = pd.DataFrame(columns=['Name', 'Price', 'Description', 'Owner', 'Contact'])
            self.items.to_excel('itemBase.xlsx', index=False)

        self.itemNum = len(self.items)
        pass

    # 物品的添加
    def addItem(self, itemName, itemPrice, itemDescription, itemOwner, itemOwnerContact):
        newItem = pd.DataFrame({
            'Name': [itemName],
            'Price': [itemPrice],
            'Description': [itemDescription],
            'Owner': [itemOwner],
            'Contact': [itemOwnerContact]
        })
        
        self.items = pd.concat([self.items, newItem], ignore_index=True)
        self.itemNum = len(self.items)
        return "物品添加成功！"
    
    # 物品的搜索
    def searchItem(self, keywords):
        if self.itemNum == 0:
            return []
        
        # 在物品名和描述中搜索
        maskName = self.items['Name'].str.contains(keywords, case=False, na=False)
        maskDesc = self.items['Description'].str.contains(keywords, case=False, na=False)
        
        searchResults = self.items[maskName | maskDesc]
        return searchResults
    
    # 物品的删除
    def deleteItem(self, itemID):
        if itemID < 0 or itemID >= self.itemNum:
            return "无效的物品ID！"
        
        self.items = self.items.drop(itemID).reset_index(drop=True)
        self.itemNum = len(self.items)
        
        return "物品删除成功！"
    
     # 展示所有物品
    def showAllItems(self):
        return self.items

    # 程序运行结束，保存
    def closeAndSave(self):
        self.items.to_excel('itemBase.xlsx', index=False)
    
