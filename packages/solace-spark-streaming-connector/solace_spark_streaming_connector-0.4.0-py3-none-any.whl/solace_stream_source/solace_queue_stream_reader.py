import pickle
import json
import logging
from solace.messaging.config.missing_resources_creation_configuration import MissingResourcesCreationStrategy
from solace.messaging.config.retry_strategy import RetryStrategy
from solace.messaging.config.transport_security_strategy import TLS
from solace.messaging.messaging_service import MessagingService
from solace.messaging.receiver.inbound_message import InboundMessage
from solace.messaging.receiver.message_receiver import MessageHandler
from solace.messaging.receiver.persistent_message_receiver import PersistentMessageReceiver
from solace.messaging.resources.topic_subscription import TopicSubscription
from solace.messaging.resources.queue import Queue
from pyspark.sql.datasource import DataSourceStreamReader, InputPartition
from typing import Iterator,Tuple,List
from datetime import datetime


class RangePartition(InputPartition):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class SolaceStreamReader(DataSourceStreamReader):

    def __init__(self, schema, options):
        self.solace_host = options.get("solace.broker.host")
        self.vpn_name = options.get("solace.vpn.name")
        self.auth_user = options.get("solace.message.auth.user")
        self.auth_password = options.get("solace.message.auth.password")
        self.queue_name = options.get("solace.subscribe.queue")
        self.consumers_count = options.get("solace.spark.consumer.count", 1)
        self.rows_per_batch = options.get("maxEventsPerTask", 1500)
        self.receiver_time_out=options.get("solace.receiver.time.out",10000)
        self.last_offset = None
        # self.transport_security=options.get("solace.trustore.certs").value
        # self.transport_security = truststore_cert_bc.value
        # self.get_starting_messageId()
        # self.set_solace_broker_props()

    def initialOffset(self) -> dict:
        """
        Returns the initial start offset of the reader.
        """
        logging.info("Inside initialOffset!!!!!")
        return {"last_retrieved_at": str(datetime.now())}


    def partitions(self, start: dict, end: dict):

        """
        Plans the partitioning of the current microbatch defined by start and end offset. It
        needs to return a sequence of :class:`InputPartition` objects.
        """
        if (self.last_offset is None):
            self.last_offset = end['last_retrieved_at']

        current_start = start['last_retrieved_at']
        current_end = end['last_retrieved_at']
        self.last_offset = current_end

        return [RangePartition(current_start, current_end) for i in range(int(self.consumers_count))]

    def latestOffset(self) -> dict:
        """
        Returns the current latest offset that the next microbatch will read to.
        """
        # self.current += int(self.rows_per_batch)
        return {"last_retrieved_at": str(datetime.now())}

    def read(self, partition) -> Iterator[Tuple[str, str]]:
        """
        Takes a partition as an input and reads an iterator of tuples from the data source.
        """
        start, end = partition.start, partition.end
        broker_props = {
            "solace.messaging.transport.host": self.solace_host,
            "solace.messaging.service.vpn-name": self.vpn_name,
            "solace.messaging.authentication.scheme.basic.username": self.auth_user,
            "solace.messaging.authentication.scheme.basic.password": self.auth_password
        }
        transport_security = TLS.create().with_certificate_validation(True, validate_server_name=False,
                                                                      trust_store_file_path="/home")
        messaging_service = (MessagingService.builder().from_properties(broker_props)
                             .with_reconnection_retry_strategy(RetryStrategy.parametrized_retry(20, 3))
                             .with_transport_security_strategy(transport_security)
                             .build()
                             )
        durable_non_exclusive_queue = Queue.durable_non_exclusive_queue(self.queue_name)
        persistent_receiver: PersistentMessageReceiver = messaging_service.create_persistent_message_receiver_builder() \
            .build(durable_non_exclusive_queue)
        # .with_missing_resources_creation_strategy(MissingResourcesCreationStrategy.CREATE_ON_START) \

        messaging_service.connect()
        persistent_receiver.start()
        count_of_message = 0
        reader_iter = []
        inbound_message_lst = []
        try:
            # logging.info(f"Subscribing to: {self.queue_name}")

            while count_of_message <= int(self.rows_per_batch):

                received_message: InboundMessage = persistent_receiver.receive_message(self.receiver_time_out)

                reader_iter.append((str(received_message.get_replication_group_message_id()),
                                    received_message.get_payload_as_string()))

                inbound_message_lst.append(received_message)
                count_of_message += 1
        except AttributeError as e:
            logging.info("'\nTerminating receiver.. no messages left to consume'")

        except Exception as e:
            raise Exception(f"solace system exception caught: {e}")

        finally:
            print('\nDisconnecting Messaging Service')
            for message in inbound_message_lst:
                persistent_receiver.ack(message)

            #persistent_receiver.terminate()
            messaging_service.disconnect()
            logging.info("Returning the queue (partition) event records.")
            return iter(reader_iter)

        # return iter(reader_iter)

    def commit(self, end):

        """
        This is invoked when the query has finished processing data before end offset. This
        can be used to clean up the resource.
        """
        pass