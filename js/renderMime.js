
import { RenderMimeRegistry, standardRendererFactories } from '@jupyterlab/rendermime';

export const renderMime = new RenderMimeRegistry({
    initialFactories: standardRendererFactories
});
