interface ParentNode extends Node {
  // assume never null and always html doc
  querySelector(selectors: string): HTMLElement;
}

// yno functions
declare function updateCanvasOverlays(): void;
declare function addChatMapLocation(locations: ({title: string})[]): void;
declare namespace i18next {
  declare function init(opts: any, callback): Promise;
}
declare function getSvgIcon(iconId: string, fill: boolean = false): HTMLDivElement
declare function showToastMessage(message: string, icon?: string, iconFill: boolean = false, systemName?: string, persist: boolean = false): HTMLDivElement
declare function addTooltip(target: Element, content: Node | string, asTooltipContent: boolean = false, delayed: boolean = false, interactive: boolean = false, options?: any): unknown
declare function chatInputActionFired(): Promise<void>