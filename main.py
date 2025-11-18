from nicegui import ui
import helper
import cfg

def check_sudo_entered():
    return False if cfg.sudo_pass == "" else True

def get_devices():
    for device in helper.get_usb_devices():
        table.rows.append({'device': device})

def on_bind_click(e):
    if check_sudo_entered():
        bus_id = helper.get_bus_id(e.args["device"])
        helper.bind_usb_device(bus_id)
        ui.notify(e.args["device"])
    else:
        ui.notify("Must provide sudo password")

def on_unbind_all_click():
    if check_sudo_entered():
        helper.unbind_all_devices()
    else:
        ui.notify("Must provide sudo password")

def set_sudo_pass(e):
    cfg.sudo_pass = e.value

ui.input(label='Sudo Password', on_change=lambda e: set_sudo_pass(e))

columns = [{'name': 'device', 'label': 'Device', 'field': 'device'},
           {'name': 'action', 'label': 'Action', 'align': 'center'}
]

table = ui.table(columns=columns, rows=[])
table.add_slot('body-cell-action', '''
    <q-td :props="props">
        <q-btn label="Bind" @click="() => $parent.$emit('bind', props.row)" flat />
    </q-td>
''')
table.on('bind', lambda e: on_bind_click(e))

ui.button('Get USB Devices', on_click=get_devices)
ui.button('Unbind All Devices', on_click=on_unbind_all_click)

ui.run()