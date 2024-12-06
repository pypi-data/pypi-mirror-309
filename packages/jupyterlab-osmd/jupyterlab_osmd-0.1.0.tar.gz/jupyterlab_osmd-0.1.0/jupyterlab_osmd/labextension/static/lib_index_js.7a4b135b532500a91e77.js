"use strict";
(self["webpackChunkjupyterlab_osmd"] = self["webpackChunkjupyterlab_osmd"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   OSMDWidget: () => (/* binding */ OSMDWidget),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   rendererFactory: () => (/* binding */ rendererFactory)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var opensheetmusicdisplay__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! opensheetmusicdisplay */ "webpack/sharing/consume/default/opensheetmusicdisplay/opensheetmusicdisplay");
/* harmony import */ var opensheetmusicdisplay__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(opensheetmusicdisplay__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var uuid__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! uuid */ "webpack/sharing/consume/default/uuid/uuid");
/* harmony import */ var uuid__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(uuid__WEBPACK_IMPORTED_MODULE_2__);



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
class OSMDWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    /**
     * Construct a new output widget.
     */
    constructor(options) {
        super();
        this._mimeType = options.mimeType;
        this.addClass(CLASS_NAME);
    }
    /**
     * Render musicxml into this widget's node.
     */
    async renderModel(model) {
        const data = model.data[this._mimeType];
        // Clear existing content
        this.node.innerHTML = '';
        // Create a container for OSMD
        const osmdContainer = document.createElement('div');
        osmdContainer.id = 'osmdContainer-' + (0,uuid__WEBPACK_IMPORTED_MODULE_2__.v4)(); // Use UUID as part of the ID
        // Apply styles to make the container scrollable
        osmdContainer.style.overflowY = 'auto';
        osmdContainer.style.maxHeight = '700px';
        osmdContainer.style.border = '1px solid #ccc';
        osmdContainer.style.padding = '10px';
        this.node.appendChild(osmdContainer);
        // Initialize OpenSheetMusicDisplay
        const osmd = new opensheetmusicdisplay__WEBPACK_IMPORTED_MODULE_1__.OpenSheetMusicDisplay(osmdContainer);
        osmd.setOptions({
            autoResize: true,
            backend: 'canvas', //'svg',
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
}
/**
 * A mime renderer factory for musicxml data.
 */
const rendererFactory = {
    safe: true,
    mimeTypes: [MIME_TYPE],
    createRenderer: options => new OSMDWidget(options)
};
/**
 * Extension definition.
 */
const extension = {
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
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.7a4b135b532500a91e77.js.map