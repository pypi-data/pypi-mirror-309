"use strict";(self.webpackChunkWebComponents=self.webpackChunkWebComponents||[]).push([[207],{16207:(i,e,t)=>{t.r(e),t.d(e,{default:()=>s});var n=t(2568);class s extends n.Z{constructor(i){super(i);var e=i.orig;this.origElem=e,this.divid=e.id,this.resultsViewer=$(e).data("results"),this.getIFrameAndQuizname(),this.renderQuizly(),this.caption="Quizly",this.addCaption("runestone")}getIFrameAndQuizname(){var i=$(this.origElem).html(),e=i.search("<iframe"),t=i.search("</iframe>");this.iframe=i.slice(e,t+8),e=i.search("quizname="),t=i.search("hints"),this.quizname=i.slice(e+9,t-5)}renderQuizly(){this.containerDiv=document.createElement("div"),this.containerDiv.id=this.divid,$(this.containerDiv).addClass(this.origElem.getAttribute("class")),$(this.containerDiv).html(this.iframe),$(this.origElem).replaceWith(this.containerDiv)}submitQuizly(i){var e=i.xml,t=1==i.result?"T":"F",n={event:"quizly",act:"answer:"+("T"==t?"correct":"no"),answer:e,correct:t,div_id:this.divid};this.logBookEvent(n),localStorage.setItem(this.divid,"true")}}$(document).on("runestone:login-complete",(function(){$("[data-component=quizly").each((function(i){try{var e=new s({orig:this});window.componentMap[this.id]=e,function(i,e){void 0===window.component_factory&&(window.component_factory={});var t="quizly_"+e;window.component_factory[t]=function(e){i.submitQuizly(e)}}(e,e.quizname)}catch(i){console.log(`Error rendering Quizly Exercise ${this.id}\n                          Details: ${i}`),console.log(i.stack)}}))}))}}]);
//# sourceMappingURL=207.js.map