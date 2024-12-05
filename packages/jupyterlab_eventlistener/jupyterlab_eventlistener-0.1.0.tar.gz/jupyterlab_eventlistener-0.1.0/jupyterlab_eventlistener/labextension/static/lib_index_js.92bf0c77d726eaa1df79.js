"use strict";
(self["webpackChunkjupyterlab_eventlistener"] = self["webpackChunkjupyterlab_eventlistener"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _token__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./token */ "./lib/token.js");

const PLUGIN_ID = 'jupyterlab-eventlistener';
const eventlistener = {
    id: PLUGIN_ID,
    description: "An API for listening to events coming off of JupyterLab's event manager.",
    autoStart: true,
    provides: _token__WEBPACK_IMPORTED_MODULE_0__.IEventListener,
    activate: async (app) => {
        console.log(`${PLUGIN_ID} has been activated!`);
        await app.serviceManager.ready;
        const eventListener = new _token__WEBPACK_IMPORTED_MODULE_0__.EventListener(app.serviceManager.events);
        return eventListener;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (eventlistener);


/***/ }),

/***/ "./lib/token.js":
/*!**********************!*\
  !*** ./lib/token.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   EventListener: () => (/* binding */ EventListener),
/* harmony export */   IEventListener: () => (/* binding */ IEventListener)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

const IEventListener = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('eventListener');
class EventListener {
    constructor(eventManager) {
        this._listeners = {};
        this._eventManager = eventManager;
        this._eventManager.stream.connect(async (manager, event) => {
            // Ignore an event if there is no listener.
            if (!(event.schema_id in this._listeners)) {
                return;
            }
            let listeners = this._listeners[event.schema_id];
            for (let listener of listeners) {
                await listener(manager, event.schema_id, event);
            }
        });
    }
    /**
     * Add a listener to a named event.
     *
     * @param schemaId : the event schema ID to register callbacks.
     * @param listener : callback function to register
     * @returns
     */
    addListener(schemaId, listener) {
        if (schemaId in this._listeners) {
            this._listeners[schemaId].add(listener);
            return;
        }
        // If this schemaId doesn't have any previous listeners, add one here.
        this._listeners[schemaId] = new Set([listener]);
    }
    removeListener(schemaId, listener) {
        if (schemaId in this._listeners) {
            this._listeners[schemaId].delete(listener);
            return;
        }
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.92bf0c77d726eaa1df79.js.map