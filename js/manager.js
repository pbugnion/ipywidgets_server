
import * as base from '@jupyter-widgets/base'
import * as controls from '@jupyter-widgets/controls';
import * as pWidget from '@phosphor/widgets';

import { HTMLManager } from '@jupyter-widgets/html-manager';

import * as outputWidgets from './output';

export class WidgetManager extends HTMLManager {
    constructor(kernel, el, loader) {
        super();
        this.kernel = kernel;
        this.registerWithKernel(kernel)
        this.el = el;
        this.loader = loader;
    }

    registerWithKernel(kernel) {
        if (this._commRegistration) {
            this._commRegistration.dispose();
        }
        this._commRegistration = kernel.registerCommTarget(
            this.comm_target_name,
            (comm, msg) => this.handle_comm_open(new base.shims.services.Comm(comm), msg)
        );
    }

    display_view(msg, view, options) {
        return Promise.resolve(view).then(view => {
            pWidget.Widget.attach(view.pWidget, this.el);
            view.on('remove', function() {
                console.log('view removed', view);
            });
            return view;
        });
    }

    loadClass(className, moduleName, moduleVersion) {
        if (moduleName === 'ipywidgets_server/output') {
            return Promise.resolve(outputWidgets).then(module => {
                if (module[className]) {
                    return module[className];
                } else {
                    return Promise.reject(
                        `Class ${className} not found in module ${moduleName}`
                    );
                }
            })
        } else {
            return super.loadClass(className, moduleName, moduleVersion)
        }
    }

    _create_comm(target_name, model_id, data, metadata) {
        const comm = this.kernel.connectToComm(target_name, model_id)
        if (data || metdata) {
            comm.open(data, metadata)
        }
        return Promise.resolve(new base.shims.services.Comm(comm))
    }

    _get_comm_info() {
        return this.kernel.requestCommInfo({ target: this.comm_target_name})
            .then(reply => reply.content.comms)
    }
}
