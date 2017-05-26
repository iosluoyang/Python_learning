/**
 * Created by HelloWorld on 2017/2/23.
 */
// var page = require('webpage').create();
// page.open('http://www.baidu.com', function (status) {
//     console.log("Status: " + status);
//     if (status === "success") {
//         console.log('成功打开了网页');
//         page.render('/Users/HelloWorld/Documents/个人相关/TobeBetterMe/Python学习进程/PhantomJS的用法/example.png');
//         console.log('已经成功将网页保存为图片！');
//     }
//     else{
//         console.log('未成功打开网页');
//     }
//
//     phantom.exit();
// });




// var page = require('webpage').create();
// //viewportSize being the actual size of the headless browser
// page.viewportSize = { width: 1024, height: 768 };
// //the clipRect is the portion of the page you are taking a screenshot of
// page.clipRect = { top: 0, left: 0, width: 1024, height: 768 };
// //the rest of the code is the same as the previous example
// page.open('http://www.cuiqingcai.com/', function(status) {
//      if (status === "success") {
//         console.log('成功打开了网页');
//         page.render('/Users/HelloWorld/Documents/个人相关/TobeBetterMe/Python学习进程/PhantomJS的用法/temp2.png');
//         console.log('已经成功将网页保存为图片！');
//     }
//      else{
//         console.log('未成功打开网页');
//     }
//   phantom.exit();
// });




// var url = 'http://www.cuiqingcai.com/';
// var page = require('webpage').create();
// page.onResourceRequested = function(request) {
//   console.log('Request是: ' + JSON.stringify(request, undefined, 4));
// };
// page.onResourceReceived = function(response) {
//   console.log('Receive是: ' + JSON.stringify(response, undefined, 4));
// };
// page.open(url);



// var page = require('webpage').create();
// console.log('The default user agent is ' + page.settings.userAgent);
// page.settings.userAgent = 'SpecialAgent';
// page.open('http://www.httpuseragent.org', function(status) {
//   if (status !== 'success') {
//     console.log('Unable to access network');
//   } else {
//     var ua = page.evaluate(function() {
//       return document.getElementById('myagent').textContent;
//     });
//     console.log(ua);
//   }
//   phantom.exit();
// });



var page = require('webpage').create();
page.open('http://www.sample.com', function() {
  page.includeJs("http://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js", function() {
    page.evaluate(function() {
      $("button").click();
    });
    phantom.exit()
  });
});