var mediaWikiLoadStart=(new Date()).getTime(),mwPerformance=(window.performance&&performance.mark)?performance:{mark:function(){}};mwPerformance.mark('mwLoadStart');function isCompatible(str){var ua=str||navigator.userAgent;return!!('querySelector'in document&&'localStorage'in window&&'addEventListener'in window&&!(ua.match(/webOS\/1\.[0-4]/)||ua.match(/PlayStation/i)||ua.match(/SymbianOS|Series60|NetFront|Opera Mini|S40OviBrowser|MeeGo/)||(ua.match(/Glass/)&&ua.match(/Android/))));}(function(){var NORLQ,script;if(!isCompatible()){document.documentElement.className=document.documentElement.className.replace(/(^|\s)client-js(\s|$)/,'$1client-nojs$2');NORLQ=window.NORLQ||[];while(NORLQ.length){NORLQ.shift()();}window.NORLQ={push:function(fn){fn();}};window.RLQ={push:function(){}};return;}function startUp(){mw.config=new mw.Map(true);mw.loader.addSource({"local":"/wiki/load.php"});mw.loader.register([["site","0n5jrns",[1]],["site.styles","0hvdgqo",[],"site"],["noscript","0lnrgep",[],
"noscript"],["filepage","1h3ubvm"],["user.groups","0r9vzzw",[5]],["user","1diqa7w",[6],"user"],["user.styles","05a8cr2",[],"user"],["user.cssprefs","09p30q0",[],"private"],["user.defaults","1b1p3xr"],["user.options","0j3lz3q",[8],"private"],["user.tokens","0g7wwyk",[],"private"],["mediawiki.language.data","0msaucq",[179]],["mediawiki.skinning.elements","09j7vkv"],["mediawiki.skinning.content","1bdlm12"],["mediawiki.skinning.interface","1kvgxll"],["mediawiki.skinning.content.parsoid","10o5et5"],["mediawiki.skinning.content.externallinks","1kvz8nx"],["jquery.accessKeyLabel","1tpe96l",[27,136]],["jquery.appear","1l2o7n7"],["jquery.arrowSteps","0pgl526"],["jquery.async","0nw6ror"],["jquery.autoEllipsis","1crxkpl",[39]],["jquery.badge","067peuu",[176]],["jquery.byteLength","06t1pc6"],["jquery.byteLimit","06u0oax",[23]],["jquery.checkboxShiftClick","13e36dp"],["jquery.chosen","0u8lak9"],["jquery.client","0nlkxc0"],["jquery.color","1wz0hr9",[29]],["jquery.colorUtil","0mw4ygp"],[
"jquery.confirmable","0xh681y",[180]],["jquery.cookie","014lm5g"],["jquery.expandableField","14emcwl"],["jquery.farbtastic","1lhgu1g",[29]],["jquery.footHovzer","0yrewi4"],["jquery.form","1dlpgb5"],["jquery.fullscreen","0okss0l"],["jquery.getAttrs","115r1by"],["jquery.hidpi","0ku7xi7"],["jquery.highlightText","1094tkf",[251,136]],["jquery.hoverIntent","1fba5of"],["jquery.i18n","02va70u",[178]],["jquery.localize","0pqaycx"],["jquery.makeCollapsible","1gtbub4"],["jquery.mockjax","0or86ig"],["jquery.mw-jump","1y4tou2"],["jquery.mwExtension","0hkidly"],["jquery.placeholder","0euq3kp"],["jquery.qunit","1wcxyh8"],["jquery.qunit.completenessTest","15tjdjg",[48]],["jquery.spinner","04kw2wz"],["jquery.jStorage","11gs7sx",[94]],["jquery.suggestions","09vair6",[39]],["jquery.tabIndex","1uory1f"],["jquery.tablesorter","19fig7z",[251,136,181]],["jquery.textSelection","0gczlpo",[27]],["jquery.throttle-debounce","0dco28o"],["jquery.xmldom","0fw7tdv"],["jquery.tipsy","0bes4k4"],["jquery.ui.core",
"04nyc6l",[60],"jquery.ui"],["jquery.ui.core.styles","0rgdovf",[],"jquery.ui"],["jquery.ui.accordion","1w0w9lh",[59,79],"jquery.ui"],["jquery.ui.autocomplete","1mxqkoo",[68],"jquery.ui"],["jquery.ui.button","11i2xay",[59,79],"jquery.ui"],["jquery.ui.datepicker","0obm6g4",[59],"jquery.ui"],["jquery.ui.dialog","0x6ddnm",[63,66,70,72],"jquery.ui"],["jquery.ui.draggable","13ktvlq",[59,69],"jquery.ui"],["jquery.ui.droppable","11tur7v",[66],"jquery.ui"],["jquery.ui.menu","1ii2fsj",[59,70,79],"jquery.ui"],["jquery.ui.mouse","1gxqmse",[79],"jquery.ui"],["jquery.ui.position","1rxem87",[],"jquery.ui"],["jquery.ui.progressbar","1cdw9zl",[59,79],"jquery.ui"],["jquery.ui.resizable","1c5a9nt",[59,69],"jquery.ui"],["jquery.ui.selectable","1iwzapn",[59,69],"jquery.ui"],["jquery.ui.slider","04uzyav",[59,69],"jquery.ui"],["jquery.ui.sortable","0pefz66",[59,69],"jquery.ui"],["jquery.ui.spinner","0z2ob43",[63],"jquery.ui"],["jquery.ui.tabs","178lnug",[59,79],"jquery.ui"],["jquery.ui.tooltip","14qe9b9",[59
,70,79],"jquery.ui"],["jquery.ui.widget","1rgtk05",[],"jquery.ui"],["jquery.effects.core","18j22a9",[],"jquery.ui"],["jquery.effects.blind","0i37a0w",[80],"jquery.ui"],["jquery.effects.bounce","0fenogk",[80],"jquery.ui"],["jquery.effects.clip","1c720xx",[80],"jquery.ui"],["jquery.effects.drop","0gy7heh",[80],"jquery.ui"],["jquery.effects.explode","1ejarmi",[80],"jquery.ui"],["jquery.effects.fade","0qojec0",[80],"jquery.ui"],["jquery.effects.fold","145lyms",[80],"jquery.ui"],["jquery.effects.highlight","0lp6dzq",[80],"jquery.ui"],["jquery.effects.pulsate","1imfkc6",[80],"jquery.ui"],["jquery.effects.scale","1m2nvwy",[80],"jquery.ui"],["jquery.effects.shake","0d1tcrl",[80],"jquery.ui"],["jquery.effects.slide","1qtrwz2",[80],"jquery.ui"],["jquery.effects.transfer","18yktto",[80],"jquery.ui"],["json","0v0tu11",[],null,null,"return!!(window.JSON\u0026\u0026JSON.stringify\u0026\u0026JSON.parse);"],["moment","0sjpxbr",[176]],["mediawiki.apihelp","0mwbw8j"],["mediawiki.template","1fed1kx"],[
"mediawiki.template.mustache","09dbbg7",[97]],["mediawiki.template.regexp","1bmf4fb",[97]],["mediawiki.apipretty","1n9hw67"],["mediawiki.api","1g4yxbk",[153,10]],["mediawiki.api.category","0s2cqxs",[141,101]],["mediawiki.api.edit","1pdn4oa",[141,101]],["mediawiki.api.login","1prgt0k",[101]],["mediawiki.api.options","0c189r7",[101]],["mediawiki.api.parse","137eohd",[101]],["mediawiki.api.upload","1l33cr9",[251,94,103]],["mediawiki.api.user","02okztu",[101]],["mediawiki.api.watch","0wbkk6v",[101]],["mediawiki.api.messages","1ak96g2",[101]],["mediawiki.api.rollback","0ttpfw4",[101]],["mediawiki.content.json","1kt2hr1"],["mediawiki.confirmCloseWindow","0zpg1jh"],["mediawiki.debug","09ef6xw",[34]],["mediawiki.diff.styles","14oma58"],["mediawiki.feedback","0nz0tl9",[141,130,260]],["mediawiki.feedlink","078q14u"],["mediawiki.filewarning","1a0ow8x",[256]],["mediawiki.ForeignApi","1kcv1si",[120]],["mediawiki.ForeignApi.core","19vtdvl",[101,252]],["mediawiki.helplink","1df1o5c"],[
"mediawiki.hidpi","1avz0b4",[38],null,null,"return'srcset'in new Image();"],["mediawiki.hlist","1nya243"],["mediawiki.htmlform","0e19vrp",[24,136]],["mediawiki.htmlform.ooui","0qjxau8",[256]],["mediawiki.htmlform.styles","0htijxo"],["mediawiki.htmlform.ooui.styles","1bqswmb"],["mediawiki.icon","0ylyyly"],["mediawiki.inspect","0ypvl7h",[23,94,136]],["mediawiki.messagePoster","1mgc88u",[119]],["mediawiki.messagePoster.wikitext","0oetu90",[103,130]],["mediawiki.notification","0wbu68a",[189]],["mediawiki.notify","0m1rhxk"],["mediawiki.notification.convertmessagebox","0kot3np",[132]],["mediawiki.notification.convertmessagebox.styles","0h5ayqu"],["mediawiki.RegExp","0xvwkum"],["mediawiki.pager.tablePager","09n4vp2"],["mediawiki.searchSuggest","135lbq0",[37,47,52,101]],["mediawiki.sectionAnchor","1rzbgq8"],["mediawiki.storage","1w0e9fe"],["mediawiki.Title","13i8xi5",[23,153]],["mediawiki.Upload","1vmk6zv",[107]],["mediawiki.ForeignUpload","0evbclk",[119,142]],[
"mediawiki.ForeignStructuredUpload.config","1fvsh13"],["mediawiki.ForeignStructuredUpload","0uaenr7",[144,143]],["mediawiki.Upload.Dialog","1x4za4k",[147]],["mediawiki.Upload.BookletLayout","0hnfeys",[142,180,151,249,95,258,260,266,267]],["mediawiki.ForeignStructuredUpload.BookletLayout","0b9xkeu",[145,147,110,184,245,243]],["mediawiki.toc","05tizqu",[157]],["mediawiki.Uri","06hw9vj",[153,99]],["mediawiki.user","00tl1jo",[108,157,9]],["mediawiki.userSuggest","19do007",[52,101]],["mediawiki.util","0nz43fw",[17,133]],["mediawiki.viewport","0uzvboc"],["mediawiki.checkboxtoggle","0pk5kfl"],["mediawiki.checkboxtoggle.styles","0rrjp1h"],["mediawiki.cookie","18end26",[31]],["mediawiki.toolbar","0ulofa3",[55]],["mediawiki.experiments","0po0s2o"],["mediawiki.action.edit","0zudtv4",[24,55,161,101]],["mediawiki.action.edit.styles","174jx8f"],["mediawiki.action.edit.collapsibleFooter","1ouh7tp",[43,157,128]],["mediawiki.action.edit.preview","1euihdj",[35,50,55,101,115,180]],[
"mediawiki.action.history","017acq1"],["mediawiki.action.history.styles","0sxki45"],["mediawiki.action.history.diff","14oma58"],["mediawiki.action.view.dblClickEdit","0mci9dm",[189,9]],["mediawiki.action.view.metadata","0wz01fy"],["mediawiki.action.view.categoryPage.styles","11pdt91"],["mediawiki.action.view.postEdit","0276dxi",[157,180,97]],["mediawiki.action.view.redirect","0f0o3zb",[27]],["mediawiki.action.view.redirectPage","0c0eesf"],["mediawiki.action.view.rightClickEdit","1ys489i"],["mediawiki.action.edit.editWarning","1kf9a5i",[55,113,180]],["mediawiki.action.view.filepage","1p8n3oq"],["mediawiki.language","036qjce",[177,11]],["mediawiki.cldr","1y3wd7t",[178]],["mediawiki.libs.pluralruleparser","0xe23j3"],["mediawiki.language.init","1xu4rtu"],["mediawiki.jqueryMsg","0jm4mo7",[251,176,153,9]],["mediawiki.language.months","1ww37w5",[176]],["mediawiki.language.names","16yzhn6",[179]],["mediawiki.language.specialCharacters","06es0c8",[176]],["mediawiki.libs.jpegmeta","1b6x0ju"],[
"mediawiki.page.gallery","1vq1fn9",[56,186]],["mediawiki.page.gallery.styles","12oaso7"],["mediawiki.page.gallery.slideshow","06rean5",[141,101,258,274]],["mediawiki.page.ready","1snafa9",[17,25,43,45,47]],["mediawiki.page.startup","15d74oc",[153]],["mediawiki.page.patrol.ajax","13kjwas",[50,141,101,189]],["mediawiki.page.watch.ajax","0j61xp8",[109,189]],["mediawiki.page.rollback","15k4v2a",[50,111]],["mediawiki.page.image.pagination","0qrusg3",[50,153]],["mediawiki.special","1uszbsw"],["mediawiki.special.apisandbox.styles","10l6c5r"],["mediawiki.special.apisandbox","038toh4",[101,180,244,255]],["mediawiki.special.block","1p0j5u6",[153]],["mediawiki.special.changeslist","127idd2"],["mediawiki.special.changeslist.legend","15d1tzj"],["mediawiki.special.changeslist.legend.js","198o2dl",[43,157]],["mediawiki.special.changeslist.enhanced","0pt3cfm"],["mediawiki.special.changeslist.visitedstatus","0nvamhz"],["mediawiki.special.comparepages.styles","044mxw9"],["mediawiki.special.edittags",
"1egirha",[26]],["mediawiki.special.edittags.styles","1nngiol"],["mediawiki.special.import","1x14gug"],["mediawiki.special.movePage","0tntlzl",[241]],["mediawiki.special.movePage.styles","1jx78mx"],["mediawiki.special.pageLanguage","1dx4g6t",[256]],["mediawiki.special.pagesWithProp","0fwamkm"],["mediawiki.special.preferences","0c0y24u",[113,176,134]],["mediawiki.special.userrights","0njpno9",[134]],["mediawiki.special.preferences.styles","1965zyz"],["mediawiki.special.recentchanges","11qwsmd"],["mediawiki.special.search","09vez4u",[247]],["mediawiki.special.search.styles","0xgrwdp"],["mediawiki.special.undelete","0loj2g8"],["mediawiki.special.upload","0fsnug4",[50,141,101,113,180,184,219,97]],["mediawiki.special.upload.styles","1lnvfmw"],["mediawiki.special.userlogin.common.styles","1kd1ew3"],["mediawiki.special.userlogin.signup.styles","1xhw4z2"],["mediawiki.special.userlogin.login.styles","0o5xnbj"],["mediawiki.special.userlogin.signup.js","1ddx6x9",[56,101,180]],[
"mediawiki.special.unwatchedPages","0plio5a",[141,109]],["mediawiki.special.watchlist","0nuy0v8"],["mediawiki.special.version","1t6n6aa"],["mediawiki.legacy.config","1975fi3"],["mediawiki.legacy.commonPrint","0y89mgz"],["mediawiki.legacy.protect","064hadj",[24]],["mediawiki.legacy.shared","0huj44s"],["mediawiki.legacy.oldshared","1rxqwas"],["mediawiki.legacy.wikibits","1ypwi2s",[153]],["mediawiki.ui","03mfszv"],["mediawiki.ui.checkbox","101p6ww"],["mediawiki.ui.radio","1ihc5qp"],["mediawiki.ui.anchor","0gbsod2"],["mediawiki.ui.button","0h6636c"],["mediawiki.ui.input","11depe9"],["mediawiki.ui.icon","1srbtbi"],["mediawiki.ui.text","0qyqm4l"],["mediawiki.widgets","1c4zqss",[21,24,141,101,242,258]],["mediawiki.widgets.styles","1khbaz3"],["mediawiki.widgets.DateInputWidget","0nl0xsl",[95,258]],["mediawiki.widgets.datetime","10brjru",[256]],["mediawiki.widgets.CategorySelector","0qdvmw7",[119,141,258]],["mediawiki.widgets.UserInputWidget","1i1t7tl",[258]],[
"mediawiki.widgets.SearchInputWidget","0u04pk7",[138,241]],["mediawiki.widgets.SearchInputWidget.styles","0a9jqqt"],["mediawiki.widgets.StashedFileWidget","0iciqh7",[256]],["es5-shim","1ydkdrj",[],null,null,"return(function(){'use strict';return!this\u0026\u0026!!Function.prototype.bind;}());"],["dom-level2-shim","0jkg541",[],null,null,"return!!window.Node;"],["oojs","1kszfxk",[250,94]],["mediawiki.router","0ff07in",[254]],["oojs-router","1wr5b3p",[252]],["oojs-ui","0r9vzzw",[259,258,260]],["oojs-ui-core","1mv6k9o",[176,252,257,261,262,263]],["oojs-ui-core.styles","0kd26n7"],["oojs-ui-widgets","1iu1q1c",[256]],["oojs-ui-toolbars","0lhson8",[256]],["oojs-ui-windows","05uy70d",[256]],["oojs-ui.styles.icons","15357eg"],["oojs-ui.styles.indicators","1kn9byw"],["oojs-ui.styles.textures","14dn2x8"],["oojs-ui.styles.icons-accessibility","0lr1mo2"],["oojs-ui.styles.icons-alerts","0yv81zn"],["oojs-ui.styles.icons-content","0y7gnnr"],["oojs-ui.styles.icons-editing-advanced","1oz8jb0"],[
"oojs-ui.styles.icons-editing-core","0eanjkc"],["oojs-ui.styles.icons-editing-list","182xzwp"],["oojs-ui.styles.icons-editing-styling","16f8q9g"],["oojs-ui.styles.icons-interactions","0kqlqd8"],["oojs-ui.styles.icons-layout","0wuo47g"],["oojs-ui.styles.icons-location","0df2j0c"],["oojs-ui.styles.icons-media","0p7oacb"],["oojs-ui.styles.icons-moderation","0dutd5p"],["oojs-ui.styles.icons-movement","19ni3v0"],["oojs-ui.styles.icons-user","02go4hq"],["oojs-ui.styles.icons-wikimedia","03vtgdk"],["skins.modern","0nn332z"],["skins.monobook.styles","0ogwytp"],["ext.confirmEdit.editPreview.ipwhitelist.styles","0t01cuq"],["ext.nuke","1bjg8pg"]]);;mw.config.set({"wgLoadScript":"/wiki/load.php","debug":!1,"skin":"modern","stylepath":"/wiki/skins","wgUrlProtocols":
"bitcoin\\:|ftp\\:\\/\\/|ftps\\:\\/\\/|geo\\:|git\\:\\/\\/|gopher\\:\\/\\/|http\\:\\/\\/|https\\:\\/\\/|irc\\:\\/\\/|ircs\\:\\/\\/|magnet\\:|mailto\\:|mms\\:\\/\\/|news\\:|nntp\\:\\/\\/|redis\\:\\/\\/|sftp\\:\\/\\/|sip\\:|sips\\:|sms\\:|ssh\\:\\/\\/|svn\\:\\/\\/|tel\\:|telnet\\:\\/\\/|urn\\:|worldwind\\:\\/\\/|xmpp\\:|\\/\\/","wgArticlePath":"/wiki/$1","wgScriptPath":"/wiki","wgScriptExtension":".php","wgScript":"/wiki/index.php","wgSearchType":null,"wgVariantArticlePath":!1,"wgActionPaths":{},"wgServer":"http://caving.soc.srcf.net","wgServerName":"caving.soc.srcf.net","wgUserLanguage":"en","wgContentLanguage":"en","wgTranslateNumerals":!0,"wgVersion":"1.28.2","wgEnableAPI":!0,"wgEnableWriteAPI":!0,"wgMainPageTitle":"Main Page","wgFormattedNamespaces":{"-2":"Media","-1":"Special","0":"","1":"Talk","2":"User","3":"User talk","4":"Cambridge University Caving Club - CUCC wiki","5":"Cambridge University Caving Club - CUCC wiki talk","6":"File","7":"File talk","8":"MediaWiki","9":
"MediaWiki talk","10":"Template","11":"Template talk","12":"Help","13":"Help talk","14":"Category","15":"Category talk"},"wgNamespaceIds":{"media":-2,"special":-1,"":0,"talk":1,"user":2,"user_talk":3,"cambridge_university_caving_club_-_cucc_wiki":4,"cambridge_university_caving_club_-_cucc_wiki_talk":5,"file":6,"file_talk":7,"mediawiki":8,"mediawiki_talk":9,"template":10,"template_talk":11,"help":12,"help_talk":13,"category":14,"category_talk":15,"image":6,"image_talk":7,"project":4,"project_talk":5},"wgContentNamespaces":[0],"wgSiteName":"Cambridge University Caving Club - CUCC wiki","wgDBname":"cucaving","wgExtraSignatureNamespaces":[],"wgAvailableSkins":{"modern":"Modern","monobook":"MonoBook","fallback":"Fallback","apioutput":"ApiOutput"},"wgExtensionAssetsPath":"/wiki/extensions","wgCookiePrefix":"cucaving","wgCookieDomain":"","wgCookiePath":"/","wgCookieExpiration":15552000,"wgResourceLoaderMaxQueryLength":2000,"wgCaseSensitiveNamespaces":[],"wgLegalTitleChars":
" %!\"$&'()*,\\-./0-9:;=?@A-Z\\\\\\^_`a-z~+\\u0080-\\uFFFF","wgIllegalFileChars":":/\\\\","wgResourceLoaderStorageVersion":1,"wgResourceLoaderStorageEnabled":!0,"wgResourceLoaderLegacyModules":[],"wgForeignUploadTargets":["local"],"wgEnableUploads":!0});var RLQ=window.RLQ||[];while(RLQ.length){RLQ.shift()();}window.RLQ={push:function(fn){fn();}};window.NORLQ={push:function(){}};}script=document.createElement('script');script.src="/wiki/load.php?debug=false&lang=en&modules=jquery%2Cmediawiki&only=scripts&skin=modern&version=01a0lgi";script.onload=script.onreadystatechange=function(){if(!script.readyState||/loaded|complete/.test(script.readyState)){script.onload=script.onreadystatechange=null;script=null;startUp();}};document.getElementsByTagName('head')[0].appendChild(script);}());