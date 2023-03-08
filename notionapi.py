from dotenv import dotenv_values
from notion_client import Client
from pprint import pprint

class notionapi():
    notion = Client()

    def __init__(self):
        config = dotenv_values(".env")
        notion_secret = config.get('NOTION_TOKEN')
        self.notion = Client(auth=notion_secret)
        pass
    
    def getAllPages(self):
        return self.notion.search(filter={"property": "object", "value": "page"})["results"]
    
    def getAllBlocks(self):
        BlocksInNotion = []
        PagesInNotion = self.getAllPages()
        for Page in PagesInNotion:
            BlocksInPage = self.notion.blocks.children.list(block_id=Page["id"])["results"]
            for Block in BlocksInPage:
                BlocksInNotion.append(Block)
        
        return BlocksInNotion
    
    def getDBList(self):
        blocks = self.getAllBlocks()
        db_list = [block for block in blocks if block["type"] == "child_database"]
        return db_list
    
    def getDBID(self, title):
        db_list = self.getDBList()

        for db in db_list:
            if title in db["child_database"]["title"]:
                return db["id"]
    
    def makeNewDBRow_test(self):
        DB_ID = notion.getDBID("TestDB22")
        ParentInfo = {
            'database_id' : DB_ID,
            'type' : 'database_id'
        }

        page_property = self.notion.pages.retrieve(page_id='cf32dd23-bc04-4e99-b713-92cde95438b8')['properties']

        self.notion.pages.create(parent = ParentInfo, properties = page_property)
        


notion = notionapi()

#pprint(notion.getAllPages())
#a = notion.getDBList()

#pprint(a)


#print(notion.getDBID("TestDB"))

notion.makeNewDBRow_test()
