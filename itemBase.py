import pandas as pd

class itemBase():

    def __init__(self):
        self.items = pd.read_excel('itemBase.xlsx')
        self.itemNum = len(self.items)
        pass

    #物品的添加
    def addItem(self, itemName, itemPrice, 
                itemDescription, itemOwner, itemOwnerContact):
        
        self.itemNum += 1
        itemTmp = [itemName, itemPrice, itemDescription, itemOwner, itemOwnerContact]
        self.items.append(itemTmp)
        
        return
    
    #物品的搜索
    def searchItem(self, keywords):
        
        #判断仓库是否为空
        if self.itemNum == 0:
            return 'Empty!'
        
        searchTmp=[]

        #在物品名中搜索
        for i in range(self.itemNum):
            if keywords in self.items['Name'][i]:
                searchTmp.append(i)
        
        #在描述中搜索
        for i in range(self.itemNum):
            if keywords in self.items['Description'][i]:
                searchTmp.append(i)
        
        searchTmp=list(set(searchTmp))

        if len(searchTmp) == 0:
            return 'None!'
        else:
            return searchTmp
    
    #物品的删除
    def deleteItem(self, itemID):
        
        self.items.drop(itemID)
        
        return
    
    #展示所有物品
    def showAllItems(self):
        
        print(self.items['Name', 'OwnerID'])

        return 

    #程序运行结束，保存
    def closeAndSave(self):

        self.items.to_excel('itemBase.xlsx')
        del self.items
        del self.itemNum

        return

    
