from app import *
from model import *

@app.route('/pdf/<hist_id>')
def generate_pdf(hist_id):
    historic = Historic.query.filter_by(id=hist_id).first()
    if not historic:
        abort(404)
    machine = Machine.query.filter_by(id=historic.machine_id).first()
    if not machine:
        abort(404)
    user = User.query.filter_by(id=machine.owner_id).first()
    if not user:
        abort(404)
    template = "ReportZeus.docx"
    document = MailMerge(template)
    document.merge(
        Date='{:%d-%b-%Y}'.format(date.today()),
        ClientAddress= 'Lá na zona',
        System= historic.dataos['system'],
        DestinyName= user.email,
        CompanyName= 'Tree',
        Node= historic.dataos['node'],
        Version= historic.dataos['version'],
        Processor= historic.dataos['processor'],
        SO= historic.dataos['system'],
        ClientName= user.email,
        Release= historic.dataos['release']
        )
    document.write('test-1.docx')

    msg = Message('Zeus Report', sender='ricardoajpinto@gmail.com', recipients=[user.email])
    with app.open_resource("test-1.docx") as fp:
        msg.attach("test-1.docx", "txt/docx", fp.read())
    mail.send(msg)
    return jsonify({'Result':True})