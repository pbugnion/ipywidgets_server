// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import * as outputBase from '@jupyter-widgets/output';

import { DOMWidgetView, JupyterPhosphorWidget } from '@jupyter-widgets/base';

import { RenderMime, defaultRendererFactories } from '@jupyterlab/rendermime';

import { Panel } from '@phosphor/widgets';

import { WidgetManager } from './manager';

import { OutputAreaModel, OutputArea } from '@jupyterlab/outputarea';

import * as $ from 'jquery';

const OUTPUT_WIDGET_VERSION = outputBase.OUTPUT_WIDGET_VERSION;

export
class OutputModel extends outputBase.OutputModel {
    defaults() {
        return {
            ...super.defaults(),
            //msg_id: ''
        };
    }

    initialize(attributes, options) {
        super.initialize(attributes, options)
        // The output area model is trusted since widgets are only rendered in trusted contexts.
        this._outputs = new OutputAreaModel({trusted: true});
        this.listenTo(this, 'change:is_capturing', this.reset_capture);
        // TODO handle on kernel changed
        /* this.widget_manager.context.session.kernelChanged.connect((sender, kernel) => {
         *   this._msgHook.dispose();
         * });*/
        this.reset_capture();
    }

    reset_capture() {
        if (this._msgHook) {
            this._msgHook.dispose();
        }
        this._msgHook = null;

        let kernel = this.widget_manager.kernel;
        //let msgId = this.get('msg_id');
        //console.log(`messageID: ${msgId}`)
        console.log(this.get('is_capturing'));
        if (kernel && this.get('is_capturing')) {
            this._msgHook = kernel.registerMessageHook(window.messageId, msg => {
                this.add(msg);
                return false;
            });
        }
    }

    add(msg) {
        console.log('hello message!!')
        console.log(msg)
        let msgType = msg.header.msg_type;
        switch (msgType) {
            case 'execute_result':
            case 'display_data':
            case 'stream':
            case 'error':
                let model = msg.content;
                model.output_type = msgType;
                this._outputs.add(model);
                console.log(this._outputs)
                break;
            case 'clear_output':
                this.clear_output(msg.content.wait);
                break;
            default:
                break;
        }
    }

    clear_output(wait = false) {
        this._outputs.clear(wait);
    }

    get outputs() {
        return this._outputs;
    }
}

class JupyterPhosphorPanelWidget extends Panel {
    constructor(options) {
        const { view } = options;
        delete options.view;
        super(options);
        this._view = view;
    }

    /**
     * Process the phosphor message.
     *
     * Any custom phosphor widget used inside a Jupyter widget should override
     * the processMessage function like this.
     */
    processMessage(msg) {
        super.processMessage(msg);
        this._view.processPhosphorMessage(msg);
    }

    /**
     * Dispose the widget.
     *
     * This causes the view to be destroyed as well with 'remove'
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        super.dispose();
        if (this._view) {
            this._view.remove();
        }
        this._view = null;
    }
}

export class OutputView extends outputBase.OutputView {

    _createElement(tagName) {
        this.pWidget = new JupyterPhosphorPanelWidget({ view: this });
        return this.pWidget.node;
    }

    _setElement(el) {
        if (this.el || el !== this.pWidget.node) {
            // Boxes don't allow setting the element beyond the initial creation.
            throw new Error('Cannot reset the DOM element.');
        }

        this.el = this.pWidget.node;
        //todo set this.$el
        //this.$el = $(this.pWidget.node);
    }

    /**
     * Called when view is rendered.
     */
    render() {
        super.render();
        // todo centralize rendermime
        const rendermime = new RenderMime({
            initialFactories: defaultRendererFactories
        })
        this._outputView = new OutputArea({
            rendermime,
            contentFactory: OutputArea.defaultContentFactory,
            model: this.model.outputs
        });
        this.pWidget.insertWidget(0, this._outputView);

        this.pWidget.addClass('jupyter-widgets');
        this.pWidget.addClass('widget-output');
        this.update(); // Set defaults.
    }

    remove() {
        this._outputView.dispose();
        return super.remove();
    }
}
