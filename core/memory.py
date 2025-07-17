import json, os, time

MEMORY_FILE = "data/mabel_memory.json"

class MemoryManager:
    def __init__(self):
        self.data = {"history": [], "artifacts": []}
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {"history": [], "artifacts": []}
    def log(self, entry):
        entry["timestamp"] = time.time()
        self.data["history"].append(entry)
        self.save()
    def save_artifact(self, artifact):
        artifact["timestamp"] = time.time()
        self.data["artifacts"].append(artifact)
        self.save()
    def save(self):
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.data, f, indent=2)
    def get_history(self): return self.data["history"]
    def get_artifacts(self): return self.data["artifacts"]
memory = MemoryManager()
