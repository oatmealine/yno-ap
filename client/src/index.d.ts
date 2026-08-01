interface ParentNode extends Node {
  // assume never null and always html doc
  querySelector(selectors: string): HTMLElement;
}