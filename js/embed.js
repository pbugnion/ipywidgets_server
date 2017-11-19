
import { Kernel, ServerConnection, KernelMessage } from '@jupyterlab/services'

import { OutputAreaModel, OutputArea } from '@jupyterlab/outputarea';

import { WidgetManager } from './manager'
import { renderMime } from './renderMime'

import 'font-awesome/css/font-awesome.css'
import './widgets.css'

export async function renderWidgets(baseUrl, wsUrl, loader) {
    let connectionInfo = ServerConnection.makeSettings({
        baseUrl,
        wsUrl
    });

    const kernelSpecs = await Kernel.getSpecs(connectionInfo)

    console.log(`Starting kernel ${kernelSpecs.default}`)

    const kernel = await Kernel.startNew({
        name: kernelSpecs.default,
        serverSettings: connectionInfo
    });

    const el = document.getElementById('ipywidget-server-result')
    const errorEl = document.getElementById('ipywidget-server-errors')
    const manager = new WidgetManager(kernel, el, loader);
    const outputModel = new OutputAreaModel({trusted: true});
    const outputView = new OutputArea({
        rendermime: renderMime,
        model: outputModel,
    })
    errorEl.appendChild(outputView.node)

    const options = {
        msgType: 'custom_message',
        channel: 'shell'
    }
    const msg = KernelMessage.createShellMessage(options)
    const execution = kernel.sendShellMessage(msg, true)
    execution.onIOPub = (msg) => {
        // If we have a display message, display the widget.
        if (KernelMessage.isDisplayDataMsg(msg)) {
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
        else if (KernelMessage.isErrorMsg(msg)) {
            // Show errors to help with debugging
            const model = msg.content
            model.output_type = 'error'
            outputModel.add(model)
        }
    }
}
