操作流程
==========

1. build-diff.py 逐一比較當前文件和歷史文件，生成一系列補丁（最新的 5 個），存放到指定的目錄。

2. upload.py 上傳補丁目錄裏的所有補丁。

3. upload.py 上傳當前文件。

4. register.py 登記當前文件。

5. archive.py 把當前文件歸檔。