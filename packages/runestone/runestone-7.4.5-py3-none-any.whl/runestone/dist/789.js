"use strict";(self.webpackChunkWebComponents=self.webpackChunkWebComponents||[]).push([[789],{55789:(i,t,e)=>{e.r(t);var a=e(2568),s={};class n extends a.Z{constructor(i){super(i);var t=i.orig;this.origElem=t,this.divid=t.id,this.dataEdit=!1,this.isImage=$(t).data("isimage"),this.fileName=$(t).data("filename"),!0===$(this.origElem).data("edit")&&(this.dataEdit=!0),this.displayClass="block",$(this.origElem).is("[data-hidden]")&&(this.displayClass="none"),this.numberOfRows=$(this.origElem).data("rows"),this.numberOfCols=$(this.origElem).data("cols"),this.isImage||(this.dataEdit?this.createTextArea():this.createPre(),this.fileName&&(this.containerDiv.dataset.filename=this.fileName)),this.indicate_component_ready()}createPre(){this.containerDiv=document.createElement("pre"),this.containerDiv.id=this.divid,$(this.containerDiv).attr({style:"display: "+this.displayClass}),this.containerDiv.innerHTML=this.origElem.innerHTML,$(this.origElem).replaceWith(this.containerDiv)}createTextArea(){this.containerDiv=document.createElement("textarea"),this.containerDiv.id=this.divid,this.containerDiv.rows=this.numberOfRows,this.containerDiv.cols=this.numberOfCols,this.containerDiv.innerHTML=this.origElem.innerHTML,$(this.containerDiv).addClass("datafiletextfield"),$(this.origElem).replaceWith(this.containerDiv)}}$((function(){$("[data-component=datafile]").each((function(i){try{s[this.id]=new n({orig:this})}catch(i){console.log(`Error rendering DataFile ${this.id}`)}}))})),void 0===window.component_factory&&(window.component_factory={}),window.component_factory.datafile=function(i){return new n(i)}}}]);
//# sourceMappingURL=789.js.map