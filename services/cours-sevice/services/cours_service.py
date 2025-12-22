import os
from spyne import Application, rpc, ServiceBase, Unicode, Iterable, ComplexModel, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.interface.wsdl import Wsdl11
from flask import Flask, Response, request
from base64 import b64encode

from services.db_service import init_db, get_all_courses

COURSE_DIR = "../courses"
if not os.path.exists(COURSE_DIR):
    os.makedirs(COURSE_DIR)

init_db()

class Course(ComplexModel):
    id = Integer
    user_id = Unicode
    filename = Unicode
    file_path = Unicode
    subject = Unicode
    upload_date = Unicode

class CourseService(ServiceBase):
    @rpc(_returns=Iterable(Course))
    def listCourses(ctx):
        courses = get_all_courses()
        result = []
        for course in courses:
            c = Course()
            c.id = course['id']
            c.user_id = course['user_id']
            c.filename = course['filename']
            c.file_path = course['file_path']
            c.subject = course['subject']
            c.upload_date = course['upload_date']
            result.append(c)
        return result

    @rpc(Unicode, _returns=Unicode)
    def getCourse(ctx, filename):
        file_path = os.path.join(COURSE_DIR, filename)
        if not os.path.exists(file_path):
            return "File not found"
        with open(file_path, "rb") as f:
            return b64encode(f.read()).decode("utf-8")

soap_app = Application(
    [CourseService],
    tns='school.course.soap',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)
wsgi_soap_app = WsgiApplication(soap_app)

flask_app = Flask(__name__)

@flask_app.route("/soap")
def soap_wsdl():
    wsdl = Wsdl11(soap_app.interface)
    return Response(wsdl.get_interface_document(), mimetype='text/xml')

@flask_app.route("/soap_service", methods=["POST"])
def soap_service():
    return wsgi_soap_app(request.environ, start_response=lambda status, headers: Response(status=status, headers=dict(headers)))

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    print("SOAP service running at http://localhost:5052/soap_service")
    print("WSDL available at http://localhost:5052/soap?wsdl")
    run_simple('127.0.0.1', 5052, flask_app, use_reloader=True)
