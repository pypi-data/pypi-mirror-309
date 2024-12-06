import datetime
import time
import requests
from MZAPI.APM import OpenTelemetryConfigurator, get_tracer
from MZAPI.KVS import LogHandler
from MZAPI.headers import CustomRequestHeaders
from MZAPI.LOG import PublicIPTracker


class WenAnSou:
    def __init__(self):
        self.ip = PublicIPTracker()
        self.log = LogHandler()
        M = CustomRequestHeaders()
        self.headers = M.reset_headers()
        self.configurator = OpenTelemetryConfigurator(
            host_name="WenAnSou",
            service_name="XMZAPI",
            service_version="1.0.0",
            deployment_environment="prod",
            endpoint="http://tracing-analysis-dc-sh.aliyuncs.com/adapt_i8ucd7m6kr@c81a1d4e5cb019a_i8ucd7m6kr@53df7ad2afe8301/api/otlp/traces",
        )
        self.configurator.init_opentelemetry()
        self.tracer = get_tracer()

    def get_response(self, Content):
        with self.tracer.start_as_current_span("ERNIE-4-0-8K") as span:
            url = f"https://www.hhlqilongzhu.cn/api/wenan_sou.php?msg={Content}"
            response = requests.get(url, headers=self.headers)
            current_timestamp = int(time.time())
            dt_object = datetime.datetime.fromtimestamp(current_timestamp)
            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
            span.set_attribute("id", current_timestamp)
            span.set_attribute("url", url)
            span.set_attribute("response", response.text)
            self.log.process_log(response.text, "WenAnSou")
            self.ip.track_log()
            M = response.text
            W = {"id": current_timestamp, "time": formatted_time, "response": M}
            return W
