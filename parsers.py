from loaders import load_config
import time
config = load_config()


class Measurement:

    def __init__(self, name):
        self.name = name
        self.val = None
        self.pairs = {}

    def value(self, val):
        self.val = val
        return self

    def pair(self, key, value):
        self.pairs[key] = value
        return self


class Parser:

    @staticmethod
    def new():

        parsers = {
            "influxdb": InfluxDB,
            "elasticsearch": JSON
        }

        if config["reporting"]["engine"] in parsers:
            parser = parsers[config["reporting"]["engine"]]()
            return parser
        else:
            raise ValueError('No parser with name ' + config["reporting"]["engine"] + " is defined! Please refer to documentation to create a praser for this engine")



    def __init__(self):
        self.address = None
        self.host = None
        self.measurements = []
        self.global_pairs = {}
        self.timestamp = None

    def global_set_address(self, address):
        self.address = address

    def global_set_host(self, host):
        self.host = host

    def global_pair(self, key, val):
        self.global_pairs[key] = val

    def global_set_timestamp(self):
        self.timestamp = int(time.time() * pow(10, 9))

    def measurement(self, name):
        _measurement = Measurement(name)
        self.measurements.append(_measurement)
        return _measurement

    def get(self):
        return self.measurements

class JSON(Parser):

    def get(self):

        measurements = {}
        measurements["timestamp"] = (self.timestamp if self.timestamp != None else int(time.time() * pow(10, 9)))

        # Add global pairs
        for key in self.global_pairs:
            measurements[key] = self.global_pairs[key]

        for measurement in self.measurements:
            measurements[measurement.name] = {
                key: measurement.pairs[key] for key in measurement.pairs
            }

            measurements[measurement.name]["value"] = measurement.val


        return measurements





class InfluxDB(Parser):


    def get(self):

        measurements = []
        for measurement in self.measurements:
            pairs = measurement.pairs.copy()
            pairs.update(self.global_pairs) # which returns None since it mutates z

            measurement_string = "%s,%s %s%s" % (
                measurement.name,
                ",".join(["%s=%s" % (key , pairs[key]) for key in pairs]),
                "value=%s" % (measurement.val if isinstance( measurement.val, int ) else "\"%s\"" % (measurement.val)),
                (" %s" % (self.timestamp) if self.timestamp else "")
            )

            measurements.append(measurement_string)


        return measurements
