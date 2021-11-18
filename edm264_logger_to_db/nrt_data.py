import datetime
import json
import os

from sqlalchemy.orm import Session

from cli_parser import parser
from sqlalchemy import create_engine, select

from db_generator import Base, FileData, MetaData, EDM264_C, EDM264_L, EDM264_dM, EDM264_M


parser.add_argument("-jp", "--json-path", dest="json_path",
                    help="json path (could be relative to the working folder or absolute)", type=str, default='chartjs_viz')
parser.add_argument("-jf", "--json-filename", dest="json_filename",
                    help="json filename", type=str, default='pm.json')


def json_serial(obj):
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.__str__()


if __name__ == "__main__":
    # capture filenames and options from cli
    args = parser.parse_args()

    engine = create_engine(f"sqlite+pysqlite:///{os.path.join(args.db_path, args.db_filename)}", echo=True, future=True)
    log_folder = args.log_folder
    json_filename = args.json_filename
    json_path = args.json_path
    Base.metadata.create_all(engine)

    dbsession = Session(engine)

    query = dbsession.query(EDM264_M).order_by(EDM264_M.datetime).filter(
                EDM264_M.datetime > datetime.datetime.today() - datetime.timedelta(days=5)
            )
    #query = dbsession.query(EDM264_M).order_by(EDM264_M.datetime)[-30:]
    json.dump(
        {
            instance.datetime.__str__(): instance.as_dict()
            for instance in query
        },
        fp=open(os.path.join(json_path, json_filename), 'w'),
        default=json_serial
    )
