from app import *
from model import *
from flask import abort
import requests 

from mailmerge import MailMerge
from datetime import date


@app.route('/generate_pdf/<historic>', methods=['GET','POST'])
def generate_pdf(historic):
    # historic = Historic.query.filter_by(id=hist_id).first()
    # if not historic:
    #     print(123)
    #     abort(404)
    hist = Historic.query.filter_by(id=historic).first()
    user = User.query.filter_by(id=hist.user_id).first()
    print(hist)
    print(user)
    if not historic:
        abort(405)
    if not user:
        abort(403)
    # if not machine:
    #     print(2)
    #     abort(404)
    # user = User.query.filter_by(id=machine.owner_id).first()
    # if not user:
    #     print(3)
    #     abort(404)
    template = "ReportZeus.docx"
    #document = MailMerge(template)
    with MailMerge("ReportZeus.docx") as document:
        print(document.get_merge_fields())

        document.merge(
            Date='{:%d-%b-%Y}'.format(date.today()),
            ClientAddress= 'Tomar',
            System= hist.dataos['system'],
            DestinyName= 'IPT - Instituto Politécnico de Tomar',
            CompanyName= 'IPT',
            Node= hist.dataos['node'],
            Version= hist.dataos['version'],
            Processor= hist.dataos['processor'],
            SO= hist.dataos['system'],
            ClientName= '_________________',
            Release= hist.dataos['release']
            )
        document.write('test-1.docx')

    with open('test-1.docx', 'rb') as docx:
        res = requests.post(url='http://converter-eval.plutext.com:80/v1/00000000-0000-0000-0000-000000000000/convert',
                            data=docx,
                            headers={'Content-Type': 'application/octet-stream'})
        print(res)
        f = open('out_request.pdf', 'wb')
        f.write(res.content)

    msg = Message('Zeus Report', sender='zeusnoreply@gmail.com', recipients=[user.email])
    with app.open_resource("out_request.pdf") as fp:
        msg.attach("out_request.pdf", "application/pdf", fp.read())
    mail.send(msg)
    return render_template('index.html')