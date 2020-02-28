// var searchvisible = 0;

// $("#search-menu").click(function (e) {
//   //This stops the page scrolling to the top on a # link.
//   e.preventDefault();

//   var val = $('#search-icon');
//   if (val.hasClass('ion-ios-search-strong')) {
//     val.addClass('ion-ios-close-empty');
//     val.removeClass('ion-ios-search-strong');
//   }
//   else {
//     val.removeClass('ion-ios-close-empty');
//     val.addClass('ion-ios-search-strong');
//   }


//   if (searchvisible === 0) {
//     //Search is currently hidden. Slide down and show it.
//     $("#search-form").slideDown(200);
//     $("#s").focus(); //Set focus on the search input field.
//     searchvisible = 1; //Set search visible flag to visible.
//   }

//   else {
//     //Search is currently showing. Slide it back up and hide it.
//     $("#search-form").slideUp(200);
//     searchvisible = 0;
//   }
// });

/*!
 * classie - class helper functions
 * from bonzo https://github.com/ded/bonzo
 * 
 * classie.has( elem, 'my-class' ) -> true/false
 * classie.add( elem, 'my-new-class' )
 * classie.remove( elem, 'my-unwanted-class' )
 * classie.toggle( elem, 'my-class' )
 */

/*jshint browser: true, strict: true, undef: true */
/*global define: false */

// (function (window) {

//   'use strict';

//   // class helper functions from bonzo https://github.com/ded/bonzo

//   function classReg(className) {
//     return new RegExp("(^|\\s+)" + className + "(\\s+|$)");
//   }

//   // classList support for class management
//   // altho to be fair, the api sucks because it won't accept multiple classes at once
//   var hasClass, addClass, removeClass;

//   if ('classList' in document.documentElement) {
//     hasClass = function (elem, c) {
//       return elem.classList.contains(c);
//     };
//     addClass = function (elem, c) {
//       elem.classList.add(c);
//     };
//     removeClass = function (elem, c) {
//       elem.classList.remove(c);
//     };
//   }
//   else {
//     hasClass = function (elem, c) {
//       return classReg(c).test(elem.className);
//     };
//     addClass = function (elem, c) {
//       if (!hasClass(elem, c)) {
//         elem.className = elem.className + ' ' + c;
//       }
//     };
//     removeClass = function (elem, c) {
//       elem.className = elem.className.replace(classReg(c), ' ');
//     };
//   }

//   function toggleClass(elem, c) {
//     var fn = hasClass(elem, c) ? removeClass : addClass;
//     fn(elem, c);
//   }

//   var classie = {
//     // full names
//     hasClass: hasClass,
//     addClass: addClass,
//     removeClass: removeClass,
//     toggleClass: toggleClass,
//     // short names
//     has: hasClass,
//     add: addClass,
//     remove: removeClass,
//     toggle: toggleClass
//   };

//   // transport
//   if (typeof define === 'function' && define.amd) {
//     // AMD
//     define(classie);
//   } else {
//     // browser global
//     window.classie = classie;
//   }

// })(window);

// (function () {
//   var triggerBttn = document.getElementById('trigger-overlay'),
//     overlay = document.querySelector('div.overlay'),
//     closeBttn = overlay.querySelector('button.overlay-close');
//   transEndEventNames = {
//     'WebkitTransition': 'webkitTransitionEnd',
//     'MozTransition': 'transitionend',
//     'OTransition': 'oTransitionEnd',
//     'msTransition': 'MSTransitionEnd',
//     'transition': 'transitionend'
//   },
//     transEndEventName = transEndEventNames[Modernizr.prefixed('transition')],
//     support = { transitions: Modernizr.csstransitions };

//   function toggleOverlay() {
//     if (classie.has(overlay, 'open')) {
//       classie.remove(overlay, 'open');
//       classie.add(overlay, 'close');
//       var onEndTransitionFn = function (ev) {
//         if (support.transitions) {
//           if (ev.propertyName !== 'visibility') return;
//           this.removeEventListener(transEndEventName, onEndTransitionFn);
//         }
//         classie.remove(overlay, 'close');
//       };
//       if (support.transitions) {
//         overlay.addEventListener(transEndEventName, onEndTransitionFn);
//       }
//       else {
//         onEndTransitionFn();
//       }
//     }
//     else if (!classie.has(overlay, 'close')) {
//       classie.add(overlay, 'open');
//     }
//   }

//   triggerBttn.addEventListener('click', toggleOverlay);
//   closeBttn.addEventListener('click', toggleOverlay);
// })();

/**
 * 表格添加边框
 */
$("table").addClass("table table-bordered table-striped");

/**
 * 回到顶部
 */
var timer = null;
box.onclick = function () {
  cancelAnimationFrame(timer);
  //获取当前毫秒数
  var startTime = +new Date();
  //获取当前页面的滚动高度
  var b = document.body.scrollTop || document.documentElement.scrollTop;
  var d = 500;
  var c = b;
  timer = requestAnimationFrame(function func() {
    var t = d - Math.max(0, startTime - (+new Date()) + d);
    document.documentElement.scrollTop = document.body.scrollTop = t * (-c) / d + b;
    timer = requestAnimationFrame(func);
    if (t == d) {
      cancelAnimationFrame(timer);
    }
  });
}

/**
 * 只有在滚动超过页面可视高度后才显示"回到顶部"按钮
 * 否则隐藏该按钮
 * https://www.jianshu.com/p/ce95e0353fec
 */
// 获取页面的可视窗口高度
var clientHeight = document.documentElement.clientHeight || document.body.clientHeight;
var obtn = document.getElementById('box');
// 页面滚动时增加判断，超出页面可视化高度时显示回到顶部的按钮
window.onscroll = function () {
  var osTop = document.documentElement.scrollTop || document.body.scrollTop;
  if (osTop > clientHeight / 2) {
    obtn.style.visibility = 'visible';
  } else {
    obtn.style.visibility = 'hidden';
  }
}