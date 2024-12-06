from pyspark.sql.datasource import DataSource
from pyspark.sql.types import StructType
from solace_stream_source.solace_queue_stream_reader import SolaceStreamReader
class SolaceStreamDataSource(DataSource):
    """
    A data source for streaming data from a solace pubsub queue.
    """

    @classmethod
    def name(cls):
        return "solace-pub-sub"

    def schema(self):
        return "unique_key string, value string"

    def streamReader(self, schema: StructType):
        return SolaceStreamReader(schema, self.options)