
class erspacket:
    def __init__(self):
        self.command = ""
        self.data = {}


    def add_value(self,key,value):
        self.data[key] = value
    

    def get_value(self, key: str):
        return self.data.get(key)

    def __str__(self):
        ret_string = self.command
        if len(self.data) <= 0:
            return ret_string

        ret_string += "?"
        
        first = True
        for key in self.data:
            if not first:
                ret_string += "&"
            ret_string += "{}={}".format(key, self.data[key])
            first = False
        return ret_string
    