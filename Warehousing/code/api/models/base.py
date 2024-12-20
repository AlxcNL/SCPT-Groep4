from abc import ABC, abstractmethod
import json
import os
from datetime import datetime

class Base(ABC):
    def __init__(self, root_path, file_name, is_debug=False, debug_data=None):
        self.data_path = os.path.join(root_path, file_name)
        self.load(is_debug, debug_data)

    def get_timestamp(self):
        return datetime.utcnow().isoformat() + "Z"

    def load(self, is_debug, debug_data=None):
        if is_debug and debug_data is not None:
            self.data = debug_data
        else:
            with open(self.data_path, "r") as f:
                self.data = json.load(f)

    def save(self):
        with open(self.data_path, "w") as f:
            json.dump(self.data, f)

    def get_all(self):
        return self.data

    def get_one(self, item_id):
        for item in self.data:
            if item["id"] == item_id:
                return item
        return None

    def add(self, item_data):
        item_data["created_at"] = self.get_timestamp()
        item_data["updated_at"] = self.get_timestamp()
        self.data.append(item_data)
        self.save()

    def update(self, item_id, item_data):
        item_data["updated_at"] = self.get_timestamp()
        for i in range(len(self.data)):
            if self.data[i]["id"] == item_id:
                self.data[i] = item_data
                self.save()
                return
        raise ValueError(f"Item with id {item_id} not found")

    def delete(self, item_id):
        for item in self.data:
            if item["id"] == item_id:
                self.data.remove(item)
                self.save()
                return
        raise ValueError(f"Item with id {item_id} not found")