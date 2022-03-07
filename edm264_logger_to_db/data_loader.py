import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db_generator import Base, FileData, MetaData, EDM264_C, EDM264_L, EDM264_dM, EDM264_M
from cli_parser import parser
from logger import getgglogger


# add parsed arguments on top of the parser in cli_parser

logger = getgglogger(__name__)

parser.add_argument("-df", "--datalog_file", dest="datalog_file",
                    help="if specified, read only this datalogfile", type=str, default='')


def file_already_processed(hash_digest):
    return dbsession.query(FileData).filter(FileData.hash_digest == hash_digest).count() == 1


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        # session.commit()
        return instance


def process_datalogfile(filename):
    """
    reads the filename content and commits it to the db
    :return:
    """
    logger.debug(f'Reading {filename}')
    filetype_re = filetype_re_rule.match(filename)
    if filetype_re:
        filetype = filetype_re["filetype"]
        logger.debug(f'{filename} is of type {filetype_re["filetype"]}')
        datfile = DatFile(
            os.path.join(log_folder, filename),
        )
        if file_already_processed(datfile.hash_digest):
            logger.info(f'{filename} already processed')
        else:
            # TODO come considerare il caso  in cui datfile ha lo stesso nome ma non ha lo stesso contenuto?
            logger.debug(f'{filename} not already processed')
            file_header, data = datfile.file_header, datfile.data
            # look for MetaData, and add if not present
            metadata_object = get_or_create(
                dbsession, MetaData,
                instrument_model=file_header['Model'],
                serial=file_header['Serial No.'],
                location=file_header['Location'],
                firmware_rev=file_header['Firmware revision'],
                software_rev=file_header['Software revision']
            )

            # for each line in data, add a EDM264_C entry
            #  TODO se AARGH questo successivo oggetto replica il filename ma non l'hash
            file_data = FileData(filename=filename, hash_digest=datfile.hash_digest)
            dbsession.add(file_data)
            dbsession.flush()

            #  TODO se AARGH c'è il rischio di avere misure ripetute in datetime, ma che fanno riferimento ad un
            #   differente file_data
            if filetype == 'C' or filetype == 'dM':
                if filetype == 'C':
                    DataTable = EDM264_C
                elif filetype == 'dM':
                    DataTable = EDM264_dM

                for data_row in data:
                    data_row_instance = DataTable(
                        datetime=data_row[0],
                        file_data=file_data.id,
                        data_metadata=metadata_object.id,
                        um253=data_row[1],
                        um298=data_row[2],
                        um352=data_row[3],
                        um414=data_row[4],
                        um488=data_row[5],
                        um576=data_row[6],
                        um679=data_row[7],
                        um800=data_row[8],
                        um943=data_row[9],
                        um1112=data_row[10],
                        um1310=data_row[11],
                        um1545=data_row[12],
                        um1821=data_row[13],
                        um2146=data_row[14],
                        um2530=data_row[15],
                        um2982=data_row[16],
                        um3515=data_row[17],
                        um4144=data_row[18],
                        um4884=data_row[19],
                        um5757=data_row[20],
                        um6787=data_row[21],
                        um8000=data_row[22],
                        um9430=data_row[23],
                        um11120=data_row[24],
                        um13100=data_row[25],
                        um15450=data_row[26],
                        um18210=data_row[27],
                        um21460=data_row[28],
                        um25300=data_row[29],
                        um29820=data_row[30],
                        um35150=data_row[31],
                    )
                    dbsession.add(data_row_instance)
                #dbsession.commit()
            elif filetype == 'L':
                for data_row in data:
                    data_row_instance = EDM264_L(
                        datetime=data_row[0],
                        file_data=file_data.id,
                        data_metadata=metadata_object.id,
                        P=data_row[1],
                        year=data_row[2],
                        month=data_row[3],
                        day=data_row[4],
                        hour=data_row[5],
                        minute=data_row[6],
                        second=data_row[7],
                        location=data_row[8],
                        grav_factor=data_row[9],
                        error=data_row[10],
                        battery=data_row[11],
                        motor_current=data_row[12],
                        temperature_out=data_row[13],
                        humidity_out=data_row[14],
                        wind_velocity=data_row[15],
                        pressure=data_row[16],
                        wind_direction=data_row[17],
                        rain=data_row[18],
                        IV=data_row[19],
                        P_weight=data_row[20],
                        P_vol=data_row[21],
                        humidity_i=data_row[22],
                        temp_i=data_row[23],
                        latitude=data_row[24],
                        longitude=data_row[25],
                        height=data_row[26],
                        flow=data_row[27],
                        sflow=data_row[28],
                        svc_temp_set=data_row[29],
                        svc_temp=data_row[30],
                    )
                    dbsession.add(data_row_instance)
            elif filetype == 'M':
                for data_row in data:
                    data_row_instance = EDM264_M(
                        datetime=data_row[0],
                        file_data=file_data.id,
                        data_metadata=metadata_object.id,
                        tsp=data_row[1],
                        pm10=data_row[2],
                        pm4=data_row[3],
                        pm2_5=data_row[4],
                        pm1=data_row[5],
                        pm_coarse=data_row[6],
                        inhalable=data_row[7],
                        thoracic=data_row[8],
                        respirable=data_row[9],
                        pm10_iaq=data_row[10],
                        pm2_5_iaq=data_row[11],
                        pm1_iaq=data_row[12],
                    )
                    dbsession.add(data_row_instance)
    else:
        logger.info(f'{filename} not recognized')


if __name__ == "__main__":
    # capture filenames and options from cli
    args = parser.parse_args()

    # add exception?
    engine = create_engine(f"sqlite+pysqlite:///{os.path.join(args.db_path, args.db_filename)}",
                           echo=False, future=True)
    log_folder = args.log_folder
    logger.info(f'looking into {log_folder} for datalog files')


    Base.metadata.create_all(engine)
    dbsession = Session(engine)

    from datfile_reader import DatFile, filetype_re_rule

    # cycles all logfiles in log_folder
    for filename in os.listdir(log_folder):
        process_datalogfile(filename)

    dbsession.commit()
