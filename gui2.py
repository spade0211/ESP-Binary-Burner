import PySimpleGUI as sg
from datetime import datetime
import os
import threading
import subprocess

sg.theme('BlueMono')  # Add a touch of color

ports = list('Com' + str(i) for i in range(10))

layout = [
    [
        sg.Text('Enter File Location and Port-')
    ],
    [
        sg.Text('File Location '),
        sg.In(size=(25, 1), enable_events=True, key='Address'),
        sg.FileBrowse(file_types=(("BIN Files", "*.bin"),))
    ],
    [
        sg.Text('Port '),
        sg.Combo(ports, enable_events=True, readonly=False, key='Port')
    ],
    [
        sg.Button('Flash'),
        sg.Button('Close'),
        sg.Text('Version- 1.0.3', font=("Courier New", 11), expand_x=True, justification='right')],
]

window = sg.Window('ESP32 Burner', layout, font=("Arial", 11))

while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Close':
        break

    elif event == 'Flash':

        address = values['Address']
        port = values['Port']

        if not os.path.exists(address):
            sg.popup('Error', 'File Not Found')

        elif not port:
            sg.popup('Error', 'Port missing')

        elif not address.endswith('.bin'):
            sg.popup('Error', 'File not of type binary', f"Possible type: {address.split('.')[-1]}")

        elif not os.path.getsize(address):
            sg.popup('Error', 'File Empty')

        else:
            status, response = "Unsuccessful", "No Response"
            info = {
                'Date and Time': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                'Bin File Location': address,
                'Port': port,
                'Status': status,
                'Response': response
            }


            def burn():

                try:
                    process = subprocess.check_output(
                        f'esptool.exe --chip esp32 --port {port} --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size 4MB 0x1000 BlinkWithoutDelay.ino.bootloader.bin 0x8000 BlinkWithoutDelay.ino.partitions.bin 0xe000 boot_app0.bin 0x10000 {address}',
                        stderr=subprocess.STDOUT, shell=True)
                    info['Status'] = "Success"
                    info['Response'] = process

                except Exception as e:
                    info['Status'] = "Unsuccessful"
                    info['Response'] = e.stdout


            t = threading.Thread(target=burn)

            layout = [
                [
                    sg.Text('', size=(25, 1), font=('Courier', 11), key='TEXT')
                ]
            ]

            loading = sg.Window('ESP32 Flashing...', layout, finalize=True, no_titlebar=True)
            text = loading['TEXT']
            state = 0

            t.start()

            while t.is_alive():

                event, values = loading.read(timeout=100)
                if event == 0:
                    break
                state = (state + 1) % 26
                text.update('█' * state)

            loading.close()

            sg.popup(f"Flash {info['Status']} \n"
                     f"Response: {info['Response']}", font=("Arial", 11))

            try:
                file = open('logs.txt', 'a+')
                for key in info:
                    file.write(f'{key}: {info[key]}\n')
                file.write('\n')
                file.close()

            except Exception as e:
                sg.popup(f'Error while logging in file \n{e}')

window.close()


f"INSERT INTO {table_name} " \
f"(" \
f"from_time, " \
f"to_time, " \
f"adult_forward_male_count, " \
f"adult_backward_male_count, " \
f"adult_forward_female_count, " \
f"adult_backward_female_count, " \
f"adult_forward_total_count, " \
f"adult_backward_total_count, " \
f"adult_forward_mask_count, " \
f"adult_backward_mask_count, " \
f"adult_forward_no_mask_count, " \
f"adult_backward_no_mask_count, " \
f"child_forward_male_count, " \
f"child_backward_male_count, " \
f"child_forward_female_count, " \
f"child_backward_female_count, " \
f"child_forward_total_count, " \
f"child_backward_total_count, " \
f"child_forward_mask_count, " \
f"child_backward_mask_count, " \
f"child_forward_no_mask_count, " \
f"child_backward_no_mask_count, " \
f"adult_occupancy" \
f"child_occupancy" \
f") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"