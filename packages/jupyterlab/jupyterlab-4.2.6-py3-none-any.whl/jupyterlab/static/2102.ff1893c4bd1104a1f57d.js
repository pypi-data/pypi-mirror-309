(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[2102],{52102:e=>{!function(t,n){true?e.exports=n():0}(self,(()=>(()=>{"use strict";var e={6:(e,t)=>{function n(e){try{const t=new URL(e),n=t.password&&t.username?`${t.protocol}//${t.username}:${t.password}@${t.host}`:t.username?`${t.protocol}//${t.username}@${t.host}`:`${t.protocol}//${t.host}`;return e.toLocaleLowerCase().startsWith(n.toLocaleLowerCase())}catch(e){return!1}}Object.defineProperty(t,"__esModule",{value:!0}),t.LinkComputer=t.WebLinkProvider=void 0,t.WebLinkProvider=class{constructor(e,t,n,r={}){this._terminal=e,this._regex=t,this._handler=n,this._options=r}provideLinks(e,t){const n=r.computeLink(e,this._regex,this._terminal,this._handler);t(this._addCallbacks(n))}_addCallbacks(e){return e.map((e=>(e.leave=this._options.leave,e.hover=(t,n)=>{if(this._options.hover){const{range:r}=e;this._options.hover(t,n,r)}},e)))}};class r{static computeLink(e,t,i,o){const s=new RegExp(t.source,(t.flags||"")+"g"),[a,l]=r._getWindowedLineStrings(e-1,i),c=a.join("");let p;const d=[];for(;p=s.exec(c);){const e=p[0];if(!n(e))continue;const[t,s]=r._mapStrIdx(i,l,0,p.index),[a,c]=r._mapStrIdx(i,t,s,e.length);if(-1===t||-1===s||-1===a||-1===c)continue;const h={start:{x:s+1,y:t+1},end:{x:c,y:a+1}};d.push({range:h,text:e,activate:o})}return d}static _getWindowedLineStrings(e,t){let n,r=e,i=e,o=0,s="";const a=[];if(n=t.buffer.active.getLine(e)){const e=n.translateToString(!0);if(n.isWrapped&&" "!==e[0]){for(o=0;(n=t.buffer.active.getLine(--r))&&o<2048&&(s=n.translateToString(!0),o+=s.length,a.push(s),n.isWrapped&&-1===s.indexOf(" ")););a.reverse()}for(a.push(e),o=0;(n=t.buffer.active.getLine(++i))&&n.isWrapped&&o<2048&&(s=n.translateToString(!0),o+=s.length,a.push(s),-1===s.indexOf(" ")););}return[a,r]}static _mapStrIdx(e,t,n,r){const i=e.buffer.active,o=i.getNullCell();let s=n;for(;r;){const e=i.getLine(t);if(!e)return[-1,-1];for(let n=s;n<e.length;++n){e.getCell(n,o);const s=o.getChars();if(o.getWidth()&&(r-=s.length||1,n===e.length-1&&""===s)){const e=i.getLine(t+1);e&&e.isWrapped&&(e.getCell(0,o),2===o.getWidth()&&(r+=1))}if(r<0)return[t,n]}t++,s=0}return[t,s]}}t.LinkComputer=r}},t={};function n(r){var i=t[r];if(void 0!==i)return i.exports;var o=t[r]={exports:{}};return e[r](o,o.exports,n),o.exports}var r={};return(()=>{var e=r;Object.defineProperty(e,"__esModule",{value:!0}),e.WebLinksAddon=void 0;const t=n(6),i=/(https?|HTTPS?):[/]{2}[^\s"'!*(){}|\\\^<>`]*[^\s"':,.!?{}|\\\^~\[\]`()<>]/;function o(e,t){const n=window.open();if(n){try{n.opener=null}catch{}n.location.href=t}else console.warn("Opening link blocked as opener could not be cleared")}e.WebLinksAddon=class{constructor(e=o,t={}){this._handler=e,this._options=t}activate(e){this._terminal=e;const n=this._options,r=n.urlRegex||i;this._linkProvider=this._terminal.registerLinkProvider(new t.WebLinkProvider(this._terminal,r,this._handler,n))}dispose(){this._linkProvider?.dispose()}}})(),r})()))}}]);