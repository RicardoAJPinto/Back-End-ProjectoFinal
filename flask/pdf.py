from app import *
from model import *


from mailmerge import MailMerge
from datetime import date


@app.route('/generate_pdf/<hist_id>', methods=['GET'])
def generate_pdf(historic):
    # historic = Historic.query.filter_by(id=hist_id).first()
    # if not historic:
    #     print(123)
    #     abort(404)
    machine = Machine.query.filter_by(machine_id=historic['id']).first()
    user = Machine.query.filter_by(id=machine.owner_id).first()
    if not machine or not user:
        abort(404)
    # if not machine:
    #     print(2)
    #     abort(404)
    # user = User.query.filter_by(id=machine.owner_id).first()
    # if not user:
    #     print(3)
    #     abort(404)
    template = "ReportZeus.docx"
    document = MailMerge(template)
    document.merge(
        Date='{:%d-%b-%Y}'.format(date.today()),
        ClientAddress= 'Lá na zona',
        System= historic['system'],
        DestinyName= 'Lá na zona',
        CompanyName= 'Tree',
        Node= historic['node'],
        Version= historic['version'],
        Processor= historic['processor'],
        SO= historic['system'],
        ClientName= 'Lá na zona',
        Release= historic['release']
        )
    document.write('test-1.docx')

<<<<<<< HEAD:pdf.py
    msg = Message('Zeus Report', sender='ZeusNoReply@gmail.com', recipients=[user.email])
=======
    msg = Message('Zeus Report', sender='zeusnoreply@gmail.com', recipients=[user.email])
>>>>>>> master:flask/pdf.py
    with app.open_resource("test-1.docx") as fp:
        msg.attach("test-1.docx", "txt/docx", fp.read())
    mail.send(msg)
    return jsonify({'Result':True})