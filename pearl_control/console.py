import optparse
import time
import sys

from . import messagebus
from . import pearl_mini

parser = optparse.OptionParser()
parser.add_option("-b", "--broker", dest="broker", help="Address of the broker to connect to", default="mqtt.magevent.net")
parser.add_option("-p", "--broker-port", dest="broker_port", help="Port of the broker to connect to", type="int", default=8080)
parser.add_option("-n", "--name", dest="name", help="Name of this pearl mini", default="test-pearl")
parser.add_option("-l", "--listen", dest="listen", help="Listen for messages to help debug", action="store_true")

parser.add_option("-U", "--url", dest="url", help="Pearl url", type="str", default="http://10.1.32.233")
parser.add_option("-u", "--username", dest="username", help="Pearl admin username", type="str", default="admin")
parser.add_option("-P", "--password", dest="password", help="Pearl admin password", type="str", default="password")

parser.add_option("-C", "--composite-view", dest="composite", help="Name of composite view", default="Default")
parser.add_option("-w", "--web-view", dest="web", help="Name of web view", default="NextUp_Screen")

def run():
    (options, args) = parser.parse_args()
    bus = messagebus.MessageBus(options.broker, options.broker_port, f"pearlmini.{options.name}")

    #with bus as client:
    if options.listen:
        client.subscribe("pearlmini/#")
        while True:
            time.sleep(1)
    else:
        pearl = pearl_mini.PearlMini(options.url, options.username, options.password)
        info = pearl.get_params(["name", "description"])
        channels = pearl.get_channels()
        projector_channel = None
        for channel in channels:
            if channel['name'] == "Projector":
                projector_channel = channel['id']
        if not projector_channel:
            sys.exit("Could not locate channel named Projector")

        layouts = pearl.get_layouts(projector_channel)
        passthrough_layout = None
        schedule_layout = None
        for layout in layouts:
            if layout['name'] == options.composite:
                passthrough_layout = layout['id']
            if layout['name'] == options.web:
                schedule_layout = layout['id']
        if not passthrough_layout:
            sys.exit(f"Could not find layout called {options.composite} on channel Projector")
        if not schedule_layout:
            sys.exit(f"Could not find layout called {options.web} on channel Projector")
        sources = pearl.check_source_status()
        hdmia = None
        for source in sources.values():
            if source['name'] == "HDMI-A":
                hdmia = source['id']
        active_layout = None
        while True:
            if pearl.check_source_status()[hdmia]['status']['video']['resolution'] == "0x0":
                if active_layout != schedule_layout:
                    pearl.change_layout(projector_channel, schedule_layout)
                    active_layout = schedule_layout
            else:
                if active_layout != passthrough_layout:
                    pearl.change_layout(projector_channel, passthrough_layout)
                    active_layout = passthrough_layout
            time.sleep(3)
        #client.publish(f"pearlmini/{options.name}/test", f"Hello world from {info.get('name')}")