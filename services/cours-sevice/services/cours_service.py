import os
from spyne import Application, rpc, ServiceBase, Unicode, Iterable, ComplexModel, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.interface.wsdl import Wsdl11
from flask import Flask, Response
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from base64 import b64encode

from services.db_service import init_db, get_all_courses

COURSE_DIR = "../courses"
if not os.path.exists(COURSE_DIR):
    os.makedirs(COURSE_DIR)

# Initialize database
init_db()


# Define Course complex type for SOAP response
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
        """Return all courses with all database fields"""
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
        """Get course file content as base64"""
        file_path = os.path.join(COURSE_DIR, filename)
        if not os.path.exists(file_path):
            return "File not found"
        with open(file_path, "rb") as f:
            return b64encode(f.read()).decode("utf-8")


# Spyne SOAP app
soap_app = Application(
    [CourseService],
    tns='school.course.soap',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)
wsgi_soap_app = WsgiApplication(soap_app)

# Flask app
flask_app = Flask(__name__)


# Expose WSDL at /soap?wsdl
@flask_app.route("/soap")
def soap_wsdl():
    wsdl = Wsdl11(soap_app.interface)
    return Response(wsdl.get_interface_document(), mimetype='text/xml')


# Combine Flask + Spyne
flask_app.wsgi_app = DispatcherMiddleware(flask_app.wsgi_app, {
    '/soap_service': wsgi_soap_app
})

if __name__ == "__main__":
    from werkzeug.serving import run_simple

    print("SOAP service running at http://localhost:8000/soap_service")
    print("WSDL available at http://localhost:8000/soap?wsdl")
    run_simple('0.0.0.0', 8000, flask_app, use_reloader=True)