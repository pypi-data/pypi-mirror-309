import io 
import math 
import struct 
import logging 
import logging 

logger = logging.getLogger(__name__)

class ZipInfo:       
    @staticmethod
    def get_offset(offset: int) -> int:
        return int(math.floor(offset / (1024 * 1024)) / 1024 * 1024)

    @staticmethod
    def find_central_directory(data: bytes):
        EOCD_MIN_SIZE = 22
        eocd_signature = b'\x50\x4b\x05\x06'
        for i in range(len(data) - EOCD_MIN_SIZE, -1, -1):
            if data[i:i+4] == eocd_signature:
                logger.debug(f"Found EOCD at offset {i}")
                central_dir_offset, central_dir_size, total_entries = ZipInfo.parse_eocd(data[i:i+EOCD_MIN_SIZE])
                return central_dir_offset, central_dir_size, total_entries 
        return None, None, None

    @staticmethod
    def parse_eocd(eocd_data):
        if len(eocd_data) < 22:
            raise Exception("Incomplete EOCD record")
        (
            signature,
            disk_number,
            start_disk_number,
            total_entries_disk,
            total_entries,
            central_dir_size,
            central_dir_offset,
            comment_length
        ) = struct.unpack('<IHHHHIIH', eocd_data)
        return central_dir_offset, central_dir_size, total_entries

    @staticmethod
    def parse_central_directory(data: bytes, data_offset: int, total_records: int):
        CDR_SIGNATURE = b'\x50\x4b\x01\x02'
        file_info_list = []
        stream = io.BytesIO(data)

        stream.seek(data_offset)

        for record_index in range(total_records):
            signature = stream.read(4)
            if signature != CDR_SIGNATURE:
                logger.warning(f"Central Directory Record signature not found at offset {stream.tell() - 4}.")
                break

            header = stream.read(42)
            fields = struct.unpack('<2H2H2H3I5H2I', header)

            (
                version_made_by,
                version_needed_to_extract,
                general_purpose_bit_flag,
                compression_method,
                last_mod_file_time,
                last_mod_file_date,
                crc32,
                compressed_size,
                uncompressed_size,
                filename_length,
                extra_field_length,
                file_comment_length,
                disk_number_start,
                internal_file_attributes,
                external_file_attributes,
                header_offset,
            ) = fields

            start_byte = header_offset
            end_byte = start_byte + compressed_size if compressed_size > 0 else start_byte
            filename = stream.read(filename_length).decode('utf-8')

            stream.seek(extra_field_length + file_comment_length, io.SEEK_CUR)

            logger.debug(f"Record #{record_index}: filename = {filename}, start_byte = {start_byte}, end_byte = {end_byte}")

            file_info_list.append({
                'filename': filename,
                'start_byte': start_byte,
                'end_byte': end_byte
            })

        return file_info_list
