from TransportTask import TransportTask
import logging

if __name__ == "__main__":
    logging.basicConfig(filename="transportTask.log", format="%(message)s", level=logging.INFO)
    transport_task = TransportTask()
    transport_task.main_loop()
