# pdf_split
用法：
        pdf_split [文件名称或者目录名称] [page=row,colume]
                row,colume:     每一页里面拆分成row * colume个子页面
例子1：递归查找当前目录及其子目录，对所有的pdf文件按页码进行分拆，分拆后的文件为png文件
        pdf_split .
例子2：递归查找指定目录dir及其子目录，对所有的pdf文件按页码进行分拆，分拆后的文件为png文件
        pdf_split dir
例子3：对指定的pdffile,按页码进行分拆，分拆后的文件为png文件
        pdf_split pdffile
例子4：对指定的pdffile,按每页分拆为1*2个子页面,分拆后的文件为png文件
        pdf_split pdffile page=1,2

