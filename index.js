
import { Kernel, ServerConnection, KernelMessage } from '@jupyterlab/services'

import { WidgetManager } from './manager'

import './widgets.css'

const BASEURL = 'http://127.0.0.1:8889'
const WSURL = 'ws://127.0.0.1:8889'

function handle(msg, $el) {
    const { msg_type, content } = msg
    if (msg_type === 'execute_input') {
        $el.append(`> ${content.code}\n`)
    } else if (msg_type === 'execute_result') {
        const result = content.data['text/plain']
        $el.append(`= ${result}\n`)
    } else if (msg_type === 'stream' && msg.content.name === 'stdout') {
        const result = content.text
        $el.append(`< ${result}\n`)
    }
}

$(document).ready(async () => {
    let connectionInfo = ServerConnection.makeSettings({
        baseUrl: BASEURL,
        wsUrl: WSURL
    });

    const kernelSpecs = await Kernel.getSpecs(connectionInfo)

    console.log(kernelSpecs)
    console.log(`Starting kernel ${kernelSpecs.default}`)

    const kernel = await Kernel.startNew({
        name: kernelSpecs.default,
        serverSettings: connectionInfo
    });

    console.log(kernel)

    const $el = $('#result')
    const el = document.getElementById('result')
    const manager = new WidgetManager(kernel, el);
    console.log(manager);

    // const lines = [
    //     'import test_module ; test_module.CONST', 'a += 1; a', 'a += 1; a'
    // ];
    
    // lines.forEach(code => {
    //     const execution = kernel.requestExecute({ code })
    //     execution.onIOPub = (msg) => { handle(msg, $el) }
    // })

    const options = {
        msgType: 'custom_message',
        channel: 'shell'
    }
    const msg = KernelMessage.createShellMessage(options)
    const execution = kernel.sendShellMessage(msg, true)
    execution.onIOPub = (msg) => {
        // If we have a display message, display the widget.
        if (KernelMessage.isDisplayDataMsg(msg)) {
            console.log(msg)
            let widgetData = msg.content.data['application/vnd.jupyter.widget-view+json'];
            if (widgetData !== undefined && widgetData.version_major === 2) {
                let model = manager.get_model(widgetData.model_id);
                if (model !== undefined) {
                    model.then(model => {
                        manager.display_model(msg, model);
                    });
                }
            }
        }
    }
});


// $(document).ready(() => {
//     const jqxhr = $.ajax('/api/kernels', { method: 'POST'})
//     jqxhr.done((response) => {
//         const kernelId = response.id
//         console.log(`Connecting to kernel ${kernelId}.`)
//         const socket = new WebSocket(`ws://127.0.0.1:8889/api/kernels/${kernelId}/channels`)
//         console.log(socket)
//         socket.addEventListener('open', (event) => {
//             socket.send('hello socket')
//         })
//         socket.addEventListener('message', (event) => {console.log(event)})
//     })
//     jqxhr.fail((error) => {
//         console.error('Error from jqxhr')
//         console.error(error)
//     })
// })