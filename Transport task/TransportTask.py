from NorthWestCornerMethod import get_first_approach

class TransportTask:
    def __init__(self) -> None:
        self.transport_task = [

        ]
        self.storage_points = []
        self.destinations = []
    
    def set_first_approach(self):
        self.first_approach = get_first_approach(self.transport_task)    
