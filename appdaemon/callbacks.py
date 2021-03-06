import threading

from appdaemon.appdaemon import AppDaemon

class Callbacks:

    def __init__(self, ad: AppDaemon):

        self.AD = ad

        self.callbacks = {}
        self.callbacks_lock = threading.RLock()


    #
    # Diagnostic
    #

    def dump_callbacks(self):
        if self.callbacks == {}:
            self.AD.logging.diag("INFO", "No callbacks")
        else:
            self.AD.logging.diag("INFO", "--------------------------------------------------")
            self.AD.logging.diag("INFO", "Callbacks")
            self.AD.logging.diag("INFO", "--------------------------------------------------")
            for name in self.callbacks.keys():
                self.AD.logging.diag("INFO", "{}:".format(name))
                for uuid_ in self.callbacks[name]:
                    self.AD.logging.diag( "INFO", "  {} = {}".format(uuid_, self.callbacks[name][uuid_]))
            self.AD.logging.diag("INFO", "--------------------------------------------------")

    def get_callback_entries(self):
        callbacks = {}
        for name in self.callbacks.keys():
            callbacks[name] = {}
            for uuid_ in self.callbacks[name]:
                callbacks[name][uuid_] = {}
                if "entity" in callbacks[name][uuid_]:
                    callbacks[name][uuid_]["entity"] = self.callbacks[name][uuid_]["entity"]
                else:
                    callbacks[name][uuid_]["entity"] = None
                callbacks[name][uuid_]["type"] = self.callbacks[name][uuid_]["type"]
                callbacks[name][uuid_]["kwargs"] = self.callbacks[name][uuid_]["kwargs"]
                callbacks[name][uuid_]["function"] = self.callbacks[name][uuid_]["function"]
                callbacks[name][uuid_]["name"] = self.callbacks[name][uuid_]["name"]
                callbacks[name][uuid_]["pin_app"] = self.callbacks[name][uuid_]["pin_app"]
                callbacks[name][uuid_]["Pin_thread"] = self.callbacks[name][uuid_]["pin_thread"]
        return callbacks

    def clear_callbacks(self, name):
        self.AD.logging.log("DEBUG", "Clearing callbacks for {}".format(name))
        with self.callbacks_lock:
            if name in self.callbacks:
                del self.callbacks[name]
