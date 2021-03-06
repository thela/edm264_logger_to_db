import datetime
import json
import os

from sqlalchemy.orm import Session

from cli_parser import parser
from sqlalchemy import create_engine, select

from db_generator import Base, FileData, MetaData, EDM264_C, EDM264_L, EDM264_dM, EDM264_M


# add parsed arguments on top of the parser in cli_parser
parser.add_argument("-jp", "--json-path", dest="json_path",
                    help="json path (could be relative to the working folder or absolute)", type=str, default='chartjs_viz/json/')
parser.add_argument("-jf", "--json-filename", dest="json_filename",
                    help="json filename", type=str, default='pm.json')
parser.add_argument("-b", "--bin-span", dest="binning_size",
                    help="binning size in minutes", type=int, default=10)
parser.add_argument("-d", "--days", dest="days",
                    help="number of days to extract", type=int, default=2)


def json_serial(obj):
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.__str__()


def makebin(measures, minutes_per_bin=10):
    binned_data = {}
    for measure in measures:
        bin_time = measure.datetime.replace(second=0, minute=measure.datetime.minute//minutes_per_bin*minutes_per_bin).__str__()
        if bin_time in binned_data:
            binned_data[bin_time]['count'] += 1
            for key, value in measure.as_dict().items():
                if key != 'datetime':
                    binned_data[bin_time][key] += value
        else:
            binned_data[bin_time] = measure.as_dict()
            binned_data[bin_time]['datetime'] = bin_time
            binned_data[bin_time]['count'] = 1

    for bin_date, measure in binned_data.items():
        for key, value in measure.items():
            if key not in ['datetime', 'count']:
                #measure[key] = measure[key]*minutes_per_bin/measure['count']
                measure[key] = measure[key]/measure['count']

    return binned_data


def query_conteggio_particelle(days):
    return dbsession.query(EDM264_C).order_by(EDM264_C.datetime).filter(
                EDM264_C.datetime > latest_datetime - datetime.timedelta(days=days)
            )


if __name__ == "__main__":
    # capture filenames and options from cli
    args = parser.parse_args()

    engine = create_engine(f"sqlite+pysqlite:///{os.path.join(args.db_path, args.db_filename)}",
                           echo=False, future=True)
    log_folder = args.log_folder
    json_filename = args.json_filename
    json_path = args.json_path
    binning_size = args.binning_size
    days = args.days

    # creates database object
    Base.metadata.create_all(engine)
    dbsession = Session(engine)

    latest_datetime = dbsession.query(EDM264_C).order_by(EDM264_C.datetime)[-1].datetime
    query = query_conteggio_particelle(days)

    json.dump(
        {
            "datetime": latest_datetime,
            "data":  makebin(query, minutes_per_bin=binning_size),
        },
        fp=open(os.path.join(json_path, json_filename), 'w'),
        default=json_serial
    )
