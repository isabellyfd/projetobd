var comu = document.getElementById('comu');
var produ = document.getElementById('produ');
var neg = document.getElementById('neg');
var adm = document.getElementById('adm');
var ag = document.getElementById('ag');

var contentParagraph = document.getElementById('contentParagraph');

comu.addEventListener('click', function(){
	changeContentText('comu');
});

produ.addEventListener('click', function(){
	changeContentText('comu2');
});

neg.addEventListener('click', function(){
	changeContentText('comu23');
});

adm.addEventListener('click', function(){
	changeContentText('comu234');
});

ag.addEventListener('click', function(){
	changeContentText('comu23456');
});

var changeContentText = function(text) {
	// removeClass(contentParagraph, 'fadeInLeftBig');
	// addClass(contentParagraph, 'fadeOutRightBig');
	contentParagraph.innerHTML = text;
	// removeClass(contentParagraph, 'fadeOutRightBig');
	// addClass(contentParagraph, 'fadeInLeftBig');
}

var removeClass = function(element, classN){
	element.className = element.className.replace(new RegExp('\\b ' + classN + '\\b'),'');
}

var addClass = function(element, classN){
	element.className = element.className + ' ' + classN;
}

function hover(element) {
    element.setAttribute('src', 'static/images/insc-hover.png');
}
function unhover(element) {
    element.setAttribute('src', 'static/images/insc.png');
}