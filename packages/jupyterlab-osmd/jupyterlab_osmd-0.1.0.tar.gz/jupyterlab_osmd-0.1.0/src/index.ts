import { IRenderMime } from '@jupyterlab/rendermime-interfaces';

import { Widget } from '@lumino/widgets';

import { OpenSheetMusicDisplay } from 'opensheetmusicdisplay';

import { v4 as uuidv4 } from 'uuid';

/**
 * The default mime type for the extension.
 */
const MIME_TYPE = 'application/vnd.recordare.musicxml';

/**
 * The class name added to the extension.
 */
const CLASS_NAME = 'mimerenderer-musicxml';

/**
 * A widget for rendering musicxml.
 */
export class OSMDWidget extends Widget implements IRenderMime.IRenderer {
  /**
   * Construct a new output widget.
   */
  constructor(options: IRenderMime.IRendererOptions) {
    super();
    this._mimeType = options.mimeType;
    this.addClass(CLASS_NAME);
  }

  /**
   * Render musicxml into this widget's node.
   */
  async renderModel(model: IRenderMime.IMimeModel): Promise<void> {
   const data = model.data[this._mimeType] as string;

    // Clear existing content
    this.node.innerHTML = '';

    // Create a container for OSMD
    const osmdContainer = document.createElement('div');
    osmdContainer.id = 'osmdContainer-' + uuidv4(); // Use UUID as part of the ID

    // Apply styles to make the container scrollable
    osmdContainer.style.overflowY = 'auto';
    osmdContainer.style.maxHeight = '700px';
    osmdContainer.style.border = '1px solid #ccc';
    osmdContainer.style.padding = '10px';

    this.node.appendChild(osmdContainer);

    // Initialize OpenSheetMusicDisplay
    const osmd = new OpenSheetMusicDisplay(osmdContainer);
    osmd.setOptions({
      autoResize: true,
      backend:  'canvas', //'svg',
      drawTitle: true
    });

    // Return a Promise chain
    return osmd
        .load(data)
        .then(() => {
            osmd.render();
        })
        .catch((error) => {
            console.error('Failed to load or render MusicXML:', error);
            osmdContainer.innerHTML = '<p>Error loading music score</p>';
        })
        .finally(() => {
            console.log('Rendering process complete');
        });
  }

  private _mimeType: string;
}

/**
 * A mime renderer factory for musicxml data.
 */
export const rendererFactory: IRenderMime.IRendererFactory = {
  safe: true,
  mimeTypes: [MIME_TYPE],
  createRenderer: options => new OSMDWidget(options)
};

/**
 * Extension definition.
 */
const extension: IRenderMime.IExtension = {
  id: 'jupyterlab-osmd:plugin',
  // description: 'Adds MIME type renderer for musicxml content',
  rendererFactory,
  rank: 100,
  dataType: 'string',
  fileTypes: [
    {
      name: 'musicxml',
      mimeTypes: [MIME_TYPE],
      extensions: ['.musicxml']
    }
  ],
  documentWidgetFactoryOptions: {
    name: 'JupyterLab OpenSheetMusicDisplay (OSMD) mime renderer',
    primaryFileType: 'musicxml',
    fileTypes: ['musicxml'],
    defaultFor: ['musicxml']
  }
};

export default extension;
