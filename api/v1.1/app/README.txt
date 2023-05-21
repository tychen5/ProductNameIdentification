1. app/api/data/資料夾中需要放：
    a. https://docs.google.com/spreadsheets/d/1-S-seKUG-89KuIFAIUfZT1_Hzn6toxpxFMjeG1V-qFg/edit#gid=1168509020 裡面的其中三個csv表格更新 
    b. https://tableau-server.ui-p-nimbus-prod.a.uidev.tools/#/views/ProductNameList/ProductSKUandNAME?:iid=1 下載裡面資料的所有rows，需要先轉換為utf8的csv，並且更名為Product_SKU_and_NAME.csv


2. 經過construct_dict1.py 以後會產生combined_product_df_fillpartlevelna.pkl檔案

3. app/api/data/資料夾中需要放：
    a. morty 給的直接從shopify輸出的us store資料
    b. google sheet name revision的excel  https://docs.google.com/spreadsheets/d/1kznh2qY6eV1RACxuB2tUs0ftZ0cluzybDdgVBX9aqGk/edit#gid=0
    c. 名字轉換的dictionary(fl_convert_dict:pl_mapping.pkl) (還沒放！)
    d. glove字典 
    e. stop words字典 
    f. FM要拿掉的字典 （還沒放！）
    h. EM1要拿掉的字典 （還沒放！）

4. app/api/data/資料夾中需要放：
    a. bigrule_pl.pkl 可能用的到或用不到



！有寫"改"的地方要特別注意可能會更動！    