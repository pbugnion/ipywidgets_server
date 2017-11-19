
import { RenderMime, defaultRendererFactories } from '@jupyterlab/rendermime';

export const renderMime = new RenderMime({
    initialFactories: defaultRendererFactories
});
