from .yaz_connectors import (
    new_connection,
    set_connection_option,
    destroy_connection,
    search_pqf,
    get_num_found,
    get_result_set_record,
)


class AlephZ3950Session:
    def __init__(self, z3950_host, z3950_port):
        self.z3950_host = z3950_host
        self.z3950_port = z3950_port
        self._session = new_connection(self.z3950_host, self.z3950_port)
        set_connection_option(self._session, "preferredRecordSyntax", "MARC21")

    def close(self):
        if self._session:
            destroy_connection(self._session)
            self._session = None

    def __del__(self):
        self.close()

    def search(self, base: str, query: str):
        """Search for records. The base must return MARC21 in UTF-8 encoding

        Args:
            base (str): catalog base
            query (str): query in format PQF
                (https://software.indexdata.com/yaz/doc/tools.html)
        """
        set_connection_option(self._session, "databaseName", base)

        result_set_p = search_pqf(self._session, query)

        return [
            get_result_set_record(result_set_p, i)
            for i in range(get_num_found(result_set_p))
        ]
