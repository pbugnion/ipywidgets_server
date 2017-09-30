
import { Kernel, ServerConnection, KernelMessage } from '@jupyterlab/services'

import { OutputAreaModel, OutputArea } from '@jupyterlab/outputarea';
  import { RenderMime, defaultRendererFactories } from '@jupyterlab/rendermime';

import { WidgetManager } from './manager'

import './widgets.css'

const BASEURL = 'http://127.0.0.1:8889'
const WSURL = 'ws://127.0.0.1:8889'

$(document).ready(async () => {
    let connectionInfo = ServerConnection.makeSettings({
        baseUrl: BASEURL,
        wsUrl: WSURL
    });

    const kernelSpecs = await Kernel.getSpecs(connectionInfo)

    const kernel = await Kernel.startNew({
        name: kernelSpecs.default,
        serverSettings: connectionInfo
    });

    const el = document.getElementById('result')
    const errorEl = document.getElementById('errors')
    const manager = new WidgetManager(kernel, el);
    const outputModel = new OutputAreaModel({trusted: true});
    const outputView = new OutputArea({
        rendermime: new RenderMime({
            initialFactories: defaultRendererFactories
        }),
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
            const model = msg.content
            model.output_type = 'error'
            outputModel.add(model)
        }
    }
});
