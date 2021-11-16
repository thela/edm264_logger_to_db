import datetime
import hashlib
import re

from logger import getgglogger

logger = getgglogger(__name__)
filetype_re_rule = \
    re.compile(r'EDM264-1min_\d{4}[\/\-](0?[1-9]|1[012])[\/\-](0?[1-9]|[12][0-9]|3[01])-(?P<filetype>[CdML]{1,2}).dat')


class DatFile:
    def read_data(self):
        """
        reads data in the file and fills:

        self.file_header
        self.data_header
        self.data

        with its content.
        :return: True
        """

        file_ob = self.open_file()
        reading = None
        for line in file_ob.readlines():
            if line == '<Header>\n':
                logger.debug(f'Header Start')
                reading = 'header'
            elif line == '<Data>\n':
                logger.debug(f'Data Start')
                reading = 'data'
            else:
                if reading == 'header':
                    if ':' in line:
                        self.file_header[line.split(': ')[0]] = line.split(': ')[1].replace('\n', '')
                if reading == 'data':
                    if not self.data_header:
                        self.data_header = line.split('\t')
                        logger.debug(f'Read Data Header')
                    else:
                        datalist = line.split('\t')
                        datarow = [datetime.datetime.strptime(datalist[0], '%d/%m/%Y %H:%M:%S')]
                        for datastring in datalist[1:]:
                            if datastring == 'NA':
                                datarow.append(None)
                            else:
                                try:
                                    datarow.append(float(datastring.replace(',', '.')))
                                except ValueError:
                                    datarow.append(datastring)
                        self.data.append(
                            datarow
                        )

        logger.debug(f'Done Reading Data File')
        return True

    def open_file(self):
        return open(
                self.filepath, 'r', encoding='latin1')

    def sha256sum(self):
        """
        https://stackoverflow.com/questions/22058048/hashing-a-file-in-python#answer-44873382
        reads the datafile in chunks and returns the hexdigest of the content

        :return: hexdigest of the file content
        """
        h = hashlib.sha256()
        b = bytearray(128 * 1024)
        mv = memoryview(b)
        with open(self.filepath, 'rb', buffering=0) as f:
            for n in iter(lambda: f.readinto(mv), 0):
                h.update(mv[:n])
        logger.debug(f'hex digest computed')
        return h.hexdigest()

    def __init__(self, filepath):
        self.file_header = {}
        self.data_header = []
        self.data = []
        self.filepath = filepath

        # it opens/reads the file twice
        self.hash_digest = self.sha256sum()
        self.read_data()
