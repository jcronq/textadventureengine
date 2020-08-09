(this["webpackJsonpreact-xterm-app"]=this["webpackJsonpreact-xterm-app"]||[]).push([[0],{236:function(t,e,n){t.exports=n(520)},241:function(t,e,n){},242:function(t,e,n){},273:function(t,e,n){var a={"./attach/attach":75,"./attach/attach.js":75,"./attach/attach.js.map":274,"./attach/attach.test":113,"./attach/attach.test.js":113,"./attach/attach.test.js.map":297,"./attach/package":120,"./attach/package.json":120,"./attach/tsconfig":121,"./attach/tsconfig.json":121,"./fit/fit":78,"./fit/fit.js":78,"./fit/fit.js.map":298,"./fit/fit.test":122,"./fit/fit.test.js":122,"./fit/fit.test.js.map":299,"./fit/package":123,"./fit/package.json":123,"./fit/tsconfig":124,"./fit/tsconfig.json":124,"./fullscreen/fullscreen":79,"./fullscreen/fullscreen.css":300,"./fullscreen/fullscreen.js":79,"./fullscreen/fullscreen.js.map":301,"./fullscreen/fullscreen.test":125,"./fullscreen/fullscreen.test.js":125,"./fullscreen/fullscreen.test.js.map":302,"./fullscreen/package":126,"./fullscreen/package.json":126,"./fullscreen/tsconfig":127,"./fullscreen/tsconfig.json":127,"./search/SearchHelper":128,"./search/SearchHelper.js":128,"./search/SearchHelper.js.map":303,"./search/package":129,"./search/package.json":129,"./search/search":130,"./search/search.js":130,"./search/search.js.map":304,"./search/tsconfig":131,"./search/tsconfig.json":131,"./terminado/package":132,"./terminado/package.json":132,"./terminado/terminado":80,"./terminado/terminado.js":80,"./terminado/terminado.js.map":305,"./terminado/terminado.test":133,"./terminado/terminado.test.js":133,"./terminado/terminado.test.js.map":306,"./terminado/tsconfig":134,"./terminado/tsconfig.json":134,"./winptyCompat/package":135,"./winptyCompat/package.json":135,"./winptyCompat/tsconfig":136,"./winptyCompat/tsconfig.json":136,"./winptyCompat/winptyCompat":81,"./winptyCompat/winptyCompat.js":81,"./winptyCompat/winptyCompat.js.map":307,"./winptyCompat/winptyCompat.test":137,"./winptyCompat/winptyCompat.test.js":137,"./winptyCompat/winptyCompat.test.js.map":308,"./zmodem/demo/app":138,"./zmodem/demo/app.js":138,"./zmodem/demo/main":218,"./zmodem/demo/main.js":218,"./zmodem/package":219,"./zmodem/package.json":219,"./zmodem/tsconfig":220,"./zmodem/tsconfig.json":220,"./zmodem/zmodem":104,"./zmodem/zmodem.js":104,"./zmodem/zmodem.js.map":501,"./zmodem/zmodem.test":221,"./zmodem/zmodem.test.js":221,"./zmodem/zmodem.test.js.map":502};function o(t){var e=s(t);return n(e)}function s(t){if(!n.o(a,t)){var e=new Error("Cannot find module '"+t+"'");throw e.code="MODULE_NOT_FOUND",e}return a[t]}o.keys=function(){return Object.keys(a)},o.resolve=s,t.exports=o,o.id=273},337:function(t,e){},338:function(t,e){},341:function(t,e){},343:function(t,e){},382:function(t,e){},387:function(t,e){function n(t){var e=new Error("Cannot find module '"+t+"'");throw e.code="MODULE_NOT_FOUND",e}n.keys=function(){return[]},n.resolve=n,t.exports=n,n.id=387},389:function(t,e){},391:function(t,e){},423:function(t,e){},424:function(t,e){},520:function(t,e,n){"use strict";n.r(e);var a=n(10),o=n.n(a),s=n(230),i=n.n(s),c=(n(241),n(231)),r=n(232),m=n(235),l=n(234),f=(n(242),n(233)),p=n.n(f),u=n(105),d=n.n(u);n(519);var h=function(t){Object(m.a)(n,t);var e=Object(l.a)(n);function n(t,a){var s;return Object(c.a)(this,n),(s=e.call(this,t,a)).inputRef=void 0,s.inputRef=o.a.createRef(),s}return Object(r.a)(n,[{key:"componentDidMount",value:function(){!function(t){var e=t.getTerminal(),n="",a="";function o(){n="",t.write("\r\n$ ")}t.writeln("\x1b[31mWelcome to xterm.js\x1b[0m"),t.writeln("This is a local terminal emulation, without a real terminal in the back-end."),t.writeln("Type some keys and commands to play around."),t.writeln(""),o(),e.on("key",(function(e,s){var i=!s.altKey&&!s.ctrlKey&&!s.metaKey,c=function(e){e.forEach((function(n,a){var o=n.split("<br>").join("\r\n");console.log(o),t.write(o),a!=e.length-1&&t.write("\r\n")}))};if(13==s.keyCode){console.log(n),t.write("\r\n");var r=n.split(" ");if(a.length>0)d.a.post("/game/update",{session_id:a,command:n}).then((function(t){console.log(t),c(t.data.text),o()}));else switch(r[0]){case"list":case"ls":fetch("/game/list").then((function(t){return t.json()})).then((function(e){t.write(e.games.join("\r\n")),n="",o()}));break;case"start":var m=r[1],l=r[2],f=r[3];try{d.a.post("/game/start",{user:m,password:l,game:f}).then((function(t){console.log(t),a=t.data.session_id,c(t.data.text),o()}))}catch(p){t.write(p),o()}break;default:t.write("Unknown command ".concat(r[0])),o()}}else 8==s.keyCode?n.length>0&&(n=n.slice(0,-1),t.write("\b \b")):i&&(n+=e,t.write(e))})),e.on("paste",(function(e,n){t.write(e)}))}(this.inputRef.current)}},{key:"componentWillUnmount",value:function(){var t;null===(t=this.inputRef.current)||void 0===t||t.componentWillUnmount()}},{key:"render",value:function(){return o.a.createElement("div",{className:"App"},o.a.createElement(p.a,{ref:this.inputRef,addons:["fit","fullscreen","search"],style:{overflow:"hidden",position:"relative",width:"100%",height:"100%"}}))}}]),n}(a.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));i.a.render(o.a.createElement(o.a.StrictMode,null,o.a.createElement(h,null)),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(t){t.unregister()})).catch((function(t){console.error(t.message)}))}},[[236,1,2]]]);
//# sourceMappingURL=main.1c793f12.chunk.js.map