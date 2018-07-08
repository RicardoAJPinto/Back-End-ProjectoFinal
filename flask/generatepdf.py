import requests

with open('ReportZeus.docx', 'rb') as docx:
    res = requests.post(url='http://converter-eval.plutext.com:80/v1/00000000-0000-0000-0000-000000000000/convert',
                        data=docx,
                        headers={'Content-Type': 'application/octet-stream'})
    print(res)
    f = open('out_request.pdf', 'wb')
    f.write(res.content)